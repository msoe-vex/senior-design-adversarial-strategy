# Define rings
import math

MAX_NUM_RINGS = 72

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
SPAWN_ROBOT_ON_RAMP = 0.05
ADDITIONAL_ROBOT_ON_RAMP_DISCOUNT_FACTOR = 0.1

SPAWN_GOAL_ON_RAMP = 0.2
ADDITIONAL_GOAL_ON_RAMP_DISCOUNT_FACTOR = 0.3

SPAWN_RING_ON_RAMP = 0.01
ADDITIONAL_RING_ON_RAMP_DISCOUNT_FACTOR = 0.001

SPAWN_GOAL_IN_ROBOT = 0.2
ADDITIONAL_GOAL_IN_ROBOT_DISCOUNT_FACTOR = (
    0.5  # Multiply spawn rate by discount factor for each additional
)

SPAWN_RING_IN_ROBOT = 0.2
ADDITIONAL_RING_IN_ROBOT_DISCOUNT_FACTOR = (
    0.8  # Multiply spawn rate by discount factor for each additional
)

SPAWN_RING_ON_GOAL = 0.2
ADDITIONAL_RING_ON_GOAL_DISCOUNT_FACTOR = (
    0.9  # Multiply spawn rate by discount factor for each additional
)

SPAWN_RING_ON_HIGH_BRANCH = 0.1
SPAWN_RING_ON_LOW_BRANCH = 0.5

# Define logger settings
PARSER_LOGGER_NAME = "app/parser"
REPRESENTATION_LOGGER_NAME = "app/representation"
SIMULATION_LOGGER_NAME = "app/simulation"


# Object radius sizes
# Sourced from the field specification manual: https://content.vexrobotics.com/docs/21-22/tipping-point/2021-VRC-AppendixA-2.2.pdf
RING_RADIUS = 4
GOAL_RADIUS = 12.97
ROBOT_LENGTH = 15. # Arbitrary robot size for smaller robot
ROBOT_RADIUS = math.sqrt(2 * (ROBOT_LENGTH ** 2)) / 2
