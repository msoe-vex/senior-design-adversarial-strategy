import math
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
from entities.fieldConfigurations import starting_representation
from entities.constants import FIELD_WIDTH_IN


class TippingPointEnv(gym.Env):
    """
    OpenAI Gym Environment for the VEX Tipping Point Game.
    Action Space:
    - Discrete
        - No-Op [0], Up [1], Down [2], Left [3], Right [4],
        Goal In [5], Goal Out [6],
        Ring In [7], Ring Out [8], Ring Place[9]
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

        self.action_space = spaces.Discrete(10)

        self.observation_space = spaces.Dict(
            {
                "location": spaces.Box(
                    low=0, high=4, shape=(145, 145, 100), dtype=np.uint8
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

    def step(self, action):
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

        adjacent_entities = self._detect_adjacents(host, rep)
        self._do_action(action, host, adjacent_entities, rep)

        self.field_state.current_time -= 1
        done = self.field_state.current_time == 0
        obs = rep.export_to_dict()

        if done:
            reward = self._calculate_scores(host, rep)

        return obs, reward, done, {}

    def _calculate_scores(self, agent, field_rep):
        # FIXME: add platforms to scoring
        red_score = 0
        blue_score = 0
        for goal in field_rep.goals:
            red_score += goal.get_current_score(Color.RED)
            blue_score += goal.get_current_score(Color.BLUE)

        if red_score > blue_score:
            red_score = 1
            blue_score = -1
        elif red_score == blue_score:
            red_score = 1 / 2
            blue_score = 1 / 2
        else:
            red_score = -1
            blue_score = 1

        reward = 0
        if agent.color == Color.RED:
            reward = red_score
        elif agent.color == Color.BLUE:
            reward = blue_score

        return reward

    def _detect_adjacents(self, agent, field_rep):
        # FIXME find correct action distances
        adjacent_distance = 2
        adjacent_goals = [
            goal
            for goal in field_rep.goals
            if distance_between_entities(goal, agent) <= adjacent_distance
            and goal not in agent.goals
        ]
        adjacent_rings = [
            ring
            for ring in field_rep.rings
            if distance_between_entities(ring, agent) <= adjacent_distance
            and ring not in agent.rings
        ]
        return adjacent_goals, adjacent_rings

    def _do_action(self, action, host, adjacent_entities, rep):
        adjacent_goals = adjacent_entities[0]
        adjacent_rings = adjacent_entities[1]
        if action > 0:
            # movement
            if action < 5:
                self._move_collision(host, self._map_movement(action), rep)
            # goal capture
            elif action == 5 and len(adjacent_goals) > 0:
                goal = adjacent_goals.pop()

                # Remove goals from the field
                goal_idx = -1
                for idx, rep_goal in enumerate(rep.goals):
                    if goal.pose == rep_goal.pose:
                        goal_idx = idx

                rep.goals.pop(goal_idx)

                host.goals.append(goal)
            # goal release
            elif action == 6 and len(host.goals) > 0:
                # FIXME: be released according to orientation
                # FIXME: scale by distance from boundary, other robots etc.
                # FIXME: need zone boundaries to determine discount
                # FIXME: prevent goal-entity collision
                goal = host.goals.pop()
                offset = max(
                    min(host.pose.y + host.radius + goal.radius + 1, FIELD_WIDTH_IN), 0
                )
                goal.pose = Pose2D(host.pose.x, offset)

                # Add the goal back to the rep
                rep.goals.append(goal)
            # ring capture
            elif action == 7 and len(adjacent_rings) > 0:
                # FIXME: number of rings picked up in a step
                host.rings += adjacent_rings

                ring_poses = []
                for ring in adjacent_rings:
                    ring_poses.append(ring.pose)

                # Remove rings from the field
                remaining_rings = []
                for idx, rep_ring in enumerate(rep.rings):
                    if rep_ring.pose not in ring_poses:
                        remaining_rings.append(rep_ring)

                rep.rings = remaining_rings
            # # ring release
            # elif action == 8 and len(host.rings) > 0:
            #     # FIXME: is this action necessary?
            #     #       number of rings released up in a step
            #     ring = host.rings.pop()
            #     offset = host.pose.y + host.radius + ring.radius + 1
            #     ring.pose = Pose2D(host.pose.x, offset)
            # ring placement
            elif len(host.rings) > 0 and len(adjacent_goals) > 0:
                # FIXME: allow multiple rings?
                #      : encode selection in action space
                #      : survey adjacent goals for vacancy
                # FIXME: account for level difficulty
                ring = host.rings.pop()

                selected_goal = adjacent_goals[0]
                goal_levels = list(selected_goal.ring_containers.keys())
                selected_goal.add_ring(ring, goal_levels[-1])

    def _move_collision(self, host, direction, field_rep):
        # FIXME: add platforms to collision
        ent_lst = [*field_rep.robots, *field_rep.goals, *field_rep.rings]
        org_pos = host.pose
        coords = np.array([org_pos.x, org_pos.y])
        coords += direction
        new_pos = Pose2D(coords[0], coords[1], math.atan2(direction[1], direction[0]))
        host.pose = new_pos
        colliding_ens = [
            en for en in ent_lst if en.is_colliding(host) and en is not host
        ]

        if len(colliding_ens) != 0:
            host.pose = org_pos

    def _map_movement(self, action):
        dirs = {
            1: np.array([0, 1]),
            2: np.array([0, -1]),
            3: np.array([-1, 0]),
            4: np.array([1, 0]),
        }
        return dirs[action]

    def reset(self):
        # Reset the state of the environment to an initial state
        rep = self.field_state.get_current_representation()
        rep.randomize()
        self.field_state.current_time = self.MAX_STEPS

        return rep.export_to_dict()

    def render(self, mode="human", close=False):
        # Render the environment to the screen
        # FIXME: add live plotting
        return self.field_state.get_current_representation().draw()
        # if(self.field_state.current_time == self.MAX_STEPS-1):
        #     ax.redraw_in_frame()
        # plt.pause(0.001)
