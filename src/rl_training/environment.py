import math
from multiprocessing.spawn import is_forking
from typing import Tuple
import gym
import numpy as np
import matplotlib.pyplot as plt
from gym import spaces
from entities.fieldRepresentation import FieldState
from entities.mathUtils import (
    Pose2D,
    distance_between_points,
    distance_between_entities,
)
from entities.enumerations import Color
from entities.robots import HostRobot
from entities.platforms import PlatformState
from entities.fieldConfigurations import starting_representation
from entities.constants import FIELD_WIDTH_IN
from entities.fieldRepresentation import FieldRepresentation
from entities.robots import Robot
from entities.scoring_elements import Goal, Ring
from entities.mathUtils import vector_rotate
from entities.enumerations import GoalLevel


class TippingPointEnv(gym.Env):
    """
    OpenAI Gym Environment for the VEX Tipping Point Game.
    Action Space:
    - MultiDiscrete
        First dim:
        - No-Op [0], Forward [1], Backward [2], Rotate-Left [3], Rotate-Right [4],

        Second dim:
        - No-Op [0], Goal In [1], Goal Out [2], Ring In [3], Ring Place[4]

    Observation Space:
    - Dict
        {
        "location": Box(145, 145, 100), low=0 high=4 (#entity type)
            idx[x][y][id] = entity_type
            0=high_goals
            1=goals
            2=rings
            3=robot
            4=platform
        "orientation": Box(100), low=0 high=2 (#angle)
        "possesion": Box(100, 3, 2), low=0 high=75 (#count)
            idx[id][poss_level][poss_type]= count
            poss_level:
            0=base, 1=low, 2=high
            poss_type:
            0=goal, 1=ring
        "color": Box(100), low=0 high=2 (#color)
            0=red
            1=blue
            2=neutral
        "value": Box(100), low=0 high=255 (#point value)
        "is_opposing": Box(100), low=0 high=2 (#bool)
            0=n/a
            1=no
            2=yes
        }
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self, steps):
        super(TippingPointEnv, self).__init__()

        self.action_space = spaces.MultiDiscrete([5, 5])

        self.observation_space = spaces.Dict(
            {
                "location": spaces.Box(
                    low=0, high=4, shape=(145, 145, 100), dtype=np.uint8
                ),
                "orientation": spaces.Box(
                    low=0, high=2, shape=(100,), dtype=np.float16
                ),
                "possesion": spaces.Box(
                    low=0, high=100, shape=(100, 3, 2), dtype=np.uint8
                ),
                "color": spaces.Box(low=0, high=2, shape=(100,), dtype=np.uint8),
                "value": spaces.Box(low=0, high=255, shape=(100,), dtype=np.uint8),
                "is_opposing": spaces.Box(low=0, high=2, shape=(100,), dtype=np.uint8),
            }
        )

        # TODO: Calculate time
        self.field_state = FieldState(starting_representation(), steps)
        self.MAX_STEPS = steps

    def step(self, action: np.ndarray):
        # Execute one time step within the environment
        rep = self.field_state.get_current_representation()
        reward = 0
        host = [
            robot
            for robot in (
                rep.robots + rep.red_platform.robots + rep.blue_platform.robots
            )
            if type(robot) is HostRobot
        ][0]

        colliding_entities = self._detect_collisions(host, rep)
        self._do_action(action, host, colliding_entities, rep)

        self.field_state.current_time -= 1
        done = self.field_state.current_time == 0
        obs = rep.export_to_dict()

        if done:
            reward = self._calculate_scores(host, rep)

        return obs, reward, done, {}

    def _calculate_scores(self, agent: Robot, field_rep: FieldRepresentation) -> int:
        # FIXME: add platforms to scoring
        red_score = 0
        blue_score = 0

        held_goals = []
        for robot in field_rep.robots:
            if robot.check_front_goal():
                held_goals += [robot.front_goal]
            if robot.check_rear_goal():
                held_goals += [robot.rear_goal]

        for goal in field_rep.goals + held_goals:
            red_score += goal.get_current_score(Color.RED)
            blue_score += goal.get_current_score(Color.BLUE)

        red_score += field_rep.red_platform.get_current_score()
        blue_score += field_rep.blue_platform.get_current_score()

        if red_score > blue_score:
            red_score = 1
            blue_score = -1
        # elif red_score == blue_score:
        #     red_score = 1 / 2
        #     blue_score = 1 / 2
        else:
            red_score = -1
            blue_score = 1

        reward = 0
        if agent.color == Color.RED:
            reward = red_score
        elif agent.color == Color.BLUE:
            reward = blue_score

        return reward

    def _detect_collisions(
        self, agent: Robot, field_rep: FieldRepresentation
    ) -> Tuple[list[Goal], list[Ring]]:
        pose_lam = (
            lambda goal: goal is not agent.front_goal and goal is not agent.rear_goal
        )
        front_goals = [
            goal
            for goal in field_rep.goals
            if agent.is_colliding_front(goal) and pose_lam(goal)
        ]
        rear_goals = [
            goal
            for goal in field_rep.goals
            if agent.is_colliding_rear(goal) and pose_lam(goal)
        ]
        front_rings = [
            ring
            for ring in field_rep.rings
            if agent.is_colliding_front(ring) and ring not in agent.rings
        ]
        rear_rings = [
            ring
            for ring in field_rep.rings
            if agent.is_colliding_rear(ring) and ring not in agent.rings
        ]
        return [front_goals, rear_goals, front_rings, rear_rings]

    def _do_action(
        self,
        action: np.ndarray,
        host: HostRobot,
        colliding_entities: Tuple[list[Goal], list[Ring]],
        rep: FieldRepresentation,
    ) -> None:
        front_goals = colliding_entities[0]
        rear_goals = colliding_entities[1]
        front_rings = colliding_entities[2]
        rear_rings = colliding_entities[3]
        colliding_rings = front_rings + rear_rings

        if action[0] > 0:
            # movement
            org_pos = self._map_movement(host, action[0])
            self._move_collision(host, org_pos, rep, front_goals, rear_goals)
        if action[1] > 0:
            # goal capture
            if action[1] == 1 and (len(front_goals) > 0 or len(rear_goals) > 0):
                goal = None
                success = True
                is_rear = False
                if len(rear_goals) > 0 and not host.check_rear_goal():
                    goal = rear_goals.pop()
                    is_rear = True
                elif not host.check_front_goal():
                    goal = front_goals.pop()
                else:
                    success = False

                if success:
                    # Remove goals from the field
                    goal_idx = -1
                    for idx, rep_goal in enumerate(rep.goals):
                        if goal.pose == rep_goal.pose:
                            goal_idx = idx

                    rep.goals.pop(goal_idx)

                    if is_rear:
                        host.rear_goal = goal
                    else:
                        host.front_goal = goal
            # goal release
            elif action[1] == 2 and (host.check_front_goal() or host.check_rear_goal()):
                goal = None
                if host.check_front_goal():
                    goal = host.front_goal
                    host.front_goal = None
                elif not host.check_front_goal():
                    goal = host.rear_goal
                    host.rear_goal = None

                # Create an offset vector along the x-axis
                offset = Pose2D(host.radius + goal.radius + 1, 0, 0)

                # Rotate the offset vector to the robot angle and clamp to field boundaries
                rotated_offset = vector_rotate(host.pose.angle, offset)
                rotated_offset.x = max(min(rotated_offset.x, FIELD_WIDTH_IN), 0)
                rotated_offset.y = max(min(rotated_offset.y, FIELD_WIDTH_IN), 0)

                # Update pose of the goal
                goal.pose = Pose2D(rotated_offset.x, rotated_offset.y)

                # check collision with platform
                if rep.red_platform.is_colliding(goal.pose):
                    rep.red_platform.goals.append(goal)
                elif rep.blue_platform.is_colliding(goal.pose):
                    rep.blue_platform.goals.append(goal)
                else:
                    # Add the goal back to the rep
                    rep.goals.append(goal)
            # ring capture
            elif action[1] == 3 and len(colliding_rings) > 0:
                host.rings += colliding_rings

                ring_poses = []
                for ring in colliding_rings:
                    ring_poses.append(ring.pose)

                # Remove rings from the field
                remaining_rings = []
                for idx, rep_ring in enumerate(rep.rings):
                    if rep_ring.pose not in ring_poses:
                        remaining_rings.append(rep_ring)

                rep.rings = remaining_rings
            # # ring release
            # elif action == 8 and len(host.rings) > 0:
            #     # FIXME: add if necessary
            # ring placement
            elif action[1] == 4 and len(host.rings) > 0 and host.check_rear_goal():
                ring = host.rings.pop()

                rear_goal = host.rear_goal
                if rear_goal.color is not Color.NEUTRAL:
                    if not rear_goal.add_ring(ring, GoalLevel.LOW):
                        rear_goal.add_ring(ring, GoalLevel.BASE)
                else:
                    rear_goal.add_ring(ring, GoalLevel.BASE)

    def _move_collision(
        self,
        host: HostRobot,
        org_pos: Pose2D,
        field_rep: FieldRepresentation,
        front_goals: list[Goal],
        rear_goals: list[Goal],
    ) -> None:
        # Ensure the robot cannot escape the field
        coords = np.array([host.pose.x, host.pose.y])
        half_width = FIELD_WIDTH_IN / 2
        coords[0] = min(max(coords[0], -half_width), half_width)
        coords[1] = min(max(coords[1], 0), FIELD_WIDTH_IN)

        new_pos = Pose2D(coords[0], coords[1], host.pose.angle)
        host.pose = new_pos

        colliding_goals = [
            goal
            for goal in field_rep.goals
            if goal.is_colliding(host)
            and goal not in front_goals
            and goal not in rear_goals
        ]

        if (
            len(colliding_goals) != 0
            or field_rep.red_platform.is_colliding(host.pose)
            or field_rep.blue_platform.is_colliding(host.pose)
        ):
            host.pose = org_pos

    def _map_movement(self, host: HostRobot, action: np.ndarray) -> dict:
        org_pos = host.pose
        if action == 1:
            host.pose.x += math.cos(host.pose.angle)
            host.pose.y += math.sin(host.pose.angle)
        elif action == 2:
            host.pose.x -= math.cos(host.pose.angle)
            host.pose.y -= math.sin(host.pose.angle)
        elif action == 3:
            host.pose.angle -= 0.5 * math.pi
        elif action == 4:
            host.pose.angle += 0.5 * math.pi
        return org_pos

    def reset(self):
        # Reset the state of the environment to an initial state
        # rep = self.field_state.get_current_representation()
        # rep.randomize()

        # should fix random angles problem
        self.field_state.field_representation = starting_representation()
        rep = self.field_state.field_representation

        self.field_state.current_time = self.MAX_STEPS

        return rep.export_to_dict()

    def render(self, mode="human", close=False):
        # Render the environment to the screen
        return self.field_state.get_current_representation().draw()
        # if(self.field_state.current_time == self.MAX_STEPS-1):
        #     ax.redraw_in_frame()
        # plt.pause(0.001)
