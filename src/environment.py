from entities.fieldRepresentation import FieldState
from entities.mathUtils import Pose2D
from entities.robots import HostRobot
from entities.fieldConfigurations import starting_representation
import gym
import numpy as np
from gym import spaces
import matplotlib.pyplot as plt


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


    """
    metadata = {"render.modes": ["human"]}

    def __init__(self, steps):
        super(TippingPointEnv, self).__init__()

        self.action_space = spaces.Discrete(10)

        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(145, 145, 5),
            dtype=np.uint8,
        )

        # TODO: Calculate time
        self.field_state = FieldState(
            starting_representation(), steps)
        self.MAX_STEPS = steps

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
                no_collision, new_pos = self._collision(
                    host.position, self._map_movement(action), rep.robots)
                if no_collision:
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
            # # ring release
            # elif action == 8 and len(host.rings) > 0:
            #     # FIXME: is this action necessary?
            #     #       number of rings released up in a step
            #     ring = host.rings.pop()
            #     ring.position = host.position
            #     reward -= 1
            # ring placement
            elif len(host.rings) > 0 and len(adjacent_goals) > 0:
                # FIXME: allow multiple rings?
                #      : select goal strategically?
                ring = host.rings.pop()
                adjacent_goals[0].add_ring(ring)
                reward += 1

        self.field_state.current_time -= 1
        done = self.field_state.current_time == 0

        # FIXME: save state for continuous
        obs = rep.export_to_matrix()

        return obs, reward, False, {}

    def _collision(self, org_pos, direction, entities):
        coords = np.array([org_pos.x, org_pos.y])
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
        rep = self.field_state.get_current_representation()
        # FIXME: change to randomize
        rep = starting_representation()
        
        return rep.export_to_matrix()

    def render(self, mode="human", close=False):
        # Render the environment to the screen
        ax = self.field_state.get_current_representation().draw()
        # if(self.field_state.current_time == self.MAX_STEPS-1):
        #     ax.redraw_in_frame()
        plt.pause(.001)
