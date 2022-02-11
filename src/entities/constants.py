# Define rings
MAX_NUM_RINGS = 0

# Define goals
MAX_NUM_RED_GOALS = 2
MAX_NUM_BLUE_GOALS = 2
MAX_NUM_LOW_NEUTRAL_GOALS = 2
MAX_NUM_HIGH_NEUTRAL_GOALS = 1

# Define robots
MAX_NUM_HOST_ROBOTS = 1
MAX_NUM_PARTNER_ROBOTS = 1
MAX_NUM_OPPOSING_ROBOTS = 2

# Define ramp size
PLATFORM_LENGTH_IN = 50
PLATFORM_WIDTH_IN = 24
FIELD_WIDTH_IN = 144

# Define figure size
FIG_SIZE = (12, 12)

# Randomized spawn rates
SPAWN_GOAL_IN_ROBOT = 0.2
ADDITIONAL_GOAL_DISCOUNT_FACTOR = 0.5 # Multiply spawn rate by discount factor for each additional

SPAWN_RING_IN_ROBOT = 0.2
ADDITIONAL_RING_DISCOUNT_FACTOR = 0.8 # Multiply spawn rate by discount factor for each additional

SPAWN_RING_ON_GOAL = 0.2
ADDITIONAL_RING_DISCOUNT_FACTOR = 0.9 # Multiply spawn rate by discount factor for each additional