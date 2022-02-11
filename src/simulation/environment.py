import gym
import numpy as np
from gym import spaces


class TippingPointEnv(gym.Env):
    """
    OpenAI Gym Environment for the VEX Tipping Point Game.

    Action Space:
    - MultiDiscrete
        - Up [0], Down [1], Left [2], Right [3], No-Op [4]
        - Goal In [0], No-Op [1]
        - Ring In [0], No-Op [1]

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

        self.action_space = spaces.MultiDiscrete([5, 2, 2])

        self.observation_space = spaces.Box(
            low=0,
            high=255,
			shape=(145, 145, 5),
            dtype=np.uint8,
        )

    def step(self, action):
        # Execute one time step within the environment
        ...

    def reset(self):
        # Reset the state of the environment to an initial state
        ...

    def render(self, mode="human", close=False):
        # Render the environment to the screen
        ...
