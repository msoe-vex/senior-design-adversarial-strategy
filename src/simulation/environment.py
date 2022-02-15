from entities.field import FieldState
from entities.math_utils import Pose2D
from entities.robots import HostRobot
from examples.fieldRepresentation.field_representations import starting_representation
import gym
import numpy as np
from gym import spaces


class TippingPointEnv(gym.Env):
    """
    OpenAI Gym Environment for the VEX Tipping Point Game.

    Action Space:
    - MultiDiscrete
        - No-Op [0], Up [1], Down [2], Left [3], Right [4] 
        - No-Op [0], Goal In [1], Goal Out [2] 
        - No-Op [0], Ring In [1], Ring Out [2], Ring Place[3]

    # The issue with MultiDiscrete in this case is it assumes
    # Multi actions are temporally grouped with single ones
    # An example is that moving and picking up a goal would
    # most likely take longer than just moving
    # 
    - Discrete
        - No-Op [0], Up [1], Down [2], Left [3], Right [4], 
        Goal In [5], Goal Out [6], 
        Ring In [7], Ring Out [8], Ring Place[9]

    State Space:

        - Box
                - Dim0: X-Dimension (bounded between 0 and 144)
                - Dim1: Y-Dimension (bounded between 0 and 144)
                - Dim2: Z-Dimension (bounded between 0 and 4)
                        - Dim0: Ring Dimension
                                - Value: 
                                        - 0: No Ring
                                        - 1-255: Ring
                        - Dim1: Red Goal Dimension
                                - Value:
                                        - 0: No Goal
                                        - 1-255: Goal, Ring Score=n-1 
                        - Dim2: Blue Goal Dimension
                                - Value:
                                        - 0: No Goal
                                        - 1-255: Goal, Ring Score=n-1 
                        - Dim3: Neutral Goal Dimension
                                - Value:
                                        - 0: No Goal
                                        - 1-255: Goal, Ring Score=n-1 
                        - Dim4: Agent Dimension
                                - Value:
                                        - 0: No Agent
                                        - 1: Red Host Agent
                    - 2: Blue Host Agent
                    - 3: Red Partner Agent
                    - 4: Blue Partner Agent
                    - 5: Red Opposing Agent
                    - 6-255: Blue Opposing Agent

    """
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super(TippingPointEnv, self).__init__()

        self.action_space = spaces.Discrete([10])

        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(145, 145, 5),
            dtype=np.uint8,
        )

        # TODO: Calculate time
        self.MAX_STEPS = 180
        self.field_state = FieldState(
            starting_representation(), self.MAX_STEPS)

    def step(self, action):
        # Execute one time step within the environment
        rep = self.field_state.get_current_representation()
        reward = 0
        host = [robot for robot in rep.robots if type(robot) is HostRobot][0]
        adjacent_goals = [
            goal for goal in rep.goals if goal.position == host.position]
        adjacent_rings = [
            ring for ring in rep.rings if ring.position == host.position]

        if action > 0:
            # movement
            if action < 5:
                does_collide, new_pos = self._collision(
                    host.position, self._map_movement(action), rep.robots)
                if does_collide:
                    host.position = new_pos
            # goal capture
            elif action == 5 and len(adjacent_goals) > 0:
                goal = adjacent_goals.pop()
                host.goals.append(goal)
                reward = goal.get_current_score()
            # goal release
            elif action == 6 and len(host.goals) > 0:
                # FIXME: scale by distance from boundary, other robots etc.
                # FIXME: need zone boundaries to determine discount
                goal = host.goals.pop()
                goal.position = host.position
                reward = goal.get_current_score()
            # ring capture
            elif action == 7 and len(adjacent_rings) > 0:
                # FIXME: number of rings picked up in a step
                host.rings += adjacent_rings
                reward += len(adjacent_rings)
            # ring release
            elif action == 8 and len(host.rings) > 0:

                host.rings
            # ring placement
            elif len(host.rings) > 0 and len(adjacent_goals) > 0:
                host.rings

        self.field_state.current_time -= 1
        done = self.field_state.current_time == 0

        # FIXME: save state for continuous
        obs = rep.sparse_conversion()

        return obs, reward, done, {}

    def _collision(self, org_pos, direction, entities):
        coords = np.array(org_pos.x, org_pos.y)
        coords += direction
        new_pos = Pose2D(coords[0], coords[1])
        colliding_ens = [
            en for en in entities if en.position == new_pos]
        return len(colliding_ens) == 0, new_pos

    def _map_movement(self, action):
        dirs = {
            1: np.array([0, 1]), 2: np.array([0, -1]),
            3: np.array([-1, 0]), 4: np.array([1, 0])
        }
        return dirs[action]

    def reset(self):
        # Reset the state of the environment to an initial state
        ...

    def render(self, mode="human", close=False):
        # Render the environment to the screen
        ...
