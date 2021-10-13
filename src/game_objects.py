from abc import ABC, abstractmethod
from enum import Enum

"""
game objects classes: 10-12 by Chip

I opted to have dynamic variables
(position, distance, etc.) be pass by reference,
besides arrays which have adders. This could be changed.

See lines 140 and 178
"""


class Color(Enum):
    RED = 1
    BLUE = 2
    NEUTRAL = 3


class GoalLevel(Enum):
    ROBOT = 0
    BASE = 1
    LOW = 3
    HIGH = 10


class PlatformState(Enum):
    LEFT = 1
    RIGHT = 2
    LEVEL = 3


class ITippable(ABC):
    @abstractmethod
    def is_tipped(self):
        pass


class IScorable(ABC):
    @abstractmethod
    def get_current_score(self, color):
        pass


class Pose2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ring:
    def __init__(self, pos, dist):
        self.__position = pos
        self.__distance = dist

    def get_position(self):
        return self.__position

    def get_distance(self):
        return self.__distance


class RingContainer:
    def __init__(self, level, max_storage):
        self.__max_storage = max_storage
        self.__rings = []

        self.level = level

    def add_ring(self, ring):
        self.__rings.append(ring)

    def get_utilization(self):
        return len(self.__rings)

    def get_max_storage(self):
        return self.__max_storage

    def get_remaining_utilization(self):
        return self.__max_storage - self.get_utilization()


class Goal(ITippable, IScorable):
    def __init__(self, color, pos, dist, is_tipped, current_zone):
        self.color = color
        self.__ring_containers = {}

        self.__position = pos
        self.__distance = dist
        self.__is_tipped = is_tipped
        self.__current_zone = current_zone

    def get_position(self):
        return self.__position

    def get_distance(self):
        return self.__distance

    def get_ring_container(self, level):
        return self.__ring_containers[level]

    def get_ring_score(self):
        score = 0
        for level in self.__ring_containers:
            score += level.value * \
                self.get_ring_container(level).get_utilization()
        return score

    def is_tipped(self):
        return self.__is_tipped

    def get_current_score(self, color):
        if self.__current_zone == color \
                or self.color == Color.NEUTRAL:
            return 20 + self.get_ring_score()
        else:
            return 0


class RedGoal(Goal):
    def __init__(self, pos, dist, is_tipped, current_zone):
        super().__init__(Color.RED, pos, dist, is_tipped, current_zone)


class NeutralGoal(Goal):
    def __init__(self, pos, dist, is_tipped, current_zone):
        super().__init__(Color.NEUTRAL, pos, dist, is_tipped, current_zone)


class BlueGoal(Goal):
    def __init__(self, pos, dist, is_tipped, current_zone):
        super().__init__(Color.BLUE, pos, dist, is_tipped, current_zone)


class Robot(ITippable):
    def __init__(self, color, pos, is_tipped):
        self.color = color

        # max storage amounts subject to change?
        self.__ring_container = RingContainer(GoalLevel.ROBOT, 3)
        self.__goals = []

        self.__position = pos
        self.__is_tipped = is_tipped

    def get_position(self):
        return self.__position

    def get_ring_container(self):
        return self.__ring_container

    def add_goal(self, goal):
        self.__goals.append(goal)

    def get_goals(self):
        return self.__goals

    def is_tipped(self):
        return self.__is_tipped


class RedRobot(Robot):
    def __init__(self, pos, is_tipped):
        super().__init__(Color.RED, pos, is_tipped)


class BlueRobot(Robot):
    def __init__(self, pos, is_tipped):
        super().__init__(Color.BLUE, pos, is_tipped)


class Platform(IScorable):
    def __init__(self, color, state):
        self.color = color
        self.__state = state

        # Platform has ring reference?
        self.__rings = []
        self.__goals = []
        self.__robots = []

    def get_rings(self):
        return self.__rings

    def add_goal(self, goal):
        self.__goals.append(goal)

    def get_goals(self):
        return self.__goals

    def add_robot(self, robot):
        self.__robots.append(robot)

    def get_robots(self):
        return self.__robots

    def get_current_score(self, color):
        if self.__state == PlatformState.LEVEL:
            robots = list(filter(lambda rob: rob.color ==
                          color, self.get_robots()))
            goals = list(filter(lambda goal: goal.color ==
                                color, self.get_goals()))
            return (30 * len(robots)) + (40 * len(goals))
        else:
            return 0


class RedPlatform(Platform):
    def __init__(self, state):
        super().__init__(Color.RED, state)


class BluePlatform(Platform):
    def __init__(self, state):
        super().__init__(Color.BLUE, state)
