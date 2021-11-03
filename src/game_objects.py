from abc import ABC, abstractmethod
from enum import Enum
from serialization import ISerializable

"""
game objects classes: 10-12 by Chip

I opted to have dynamic variables
(position, distance, etc.) be pass by reference,
besides arrays which have adders. This could be changed.

See lines 140 and 178
"""

class ITippable(ABC):
    @abstractmethod
    def is_tipped(self):
        pass


class IScorable(ABC):
    @abstractmethod
    def get_current_score(self, color):
        pass


class Color(str, Enum):
    RED = 1
    BLUE = 2
    NEUTRAL = 3


class GoalLevel(str, Enum):
    ROBOT = 0
    BASE = 1
    LOW = 3
    HIGH = 10


class PlatformState(str, Enum):
    LEFT = 1
    RIGHT = 2
    LEVEL = 3


class Ring(ISerializable):
    def __init__(self, pos):
        self.position = pos
        self.classname = type(self).__name__

    def get_position(self):
        return self.position


class RingContainer(ISerializable):
    def __init__(self, level, max_storage=4):
        self.level = level
        self.max_storage = max_storage
        self.rings = []
        self.classname = type(self).__name__

    def add_ring(self, ring):
        self.rings.append(ring)

    def get_utilization(self):
        return len(self.rings)

    def get_max_storage(self):
        return self.max_storage

    def get_remaining_utilization(self):
        return self.max_storage - self.get_utilization()


class Goal(ITippable, IScorable, ISerializable):
    def __init__(self, color, pos, is_tipped=False):
        self.color = color
        self.ring_containers = {}
        self.position = pos
        self.is_tipped = is_tipped
        self.classname = type(self).__name__

        if self.position.y <= 48:
            self.current_zone = Color.RED
        elif self.position.y >= 96:
            self.current_zone = Color.BLUE
        else:
            self.current_zone = Color.NEUTRAL

    def get_position(self):
        return self.position

    def get_ring_container(self, level):
        return self.ring_containers[level]

    def get_ring_score(self):
        score = 0
        for level in self.ring_containers:
            score += level.value * \
                self.get_ring_container(level).get_utilization()
        return score

    def is_tipped(self):
        return self.is_tipped

    def get_current_score(self, color):
        if self.current_zone == color \
                or self.color == Color.NEUTRAL:
            return 20 + self.get_ring_score()
        else:
            return 0


class RedGoal(Goal, ISerializable):
    def __init__(self, pos, is_tipped=False):
        super().__init__(Color.RED, pos, is_tipped)

        self.classname = type(self).__name__


class NeutralGoal(Goal, ISerializable):
    def __init__(self, pos, is_tipped=False):
        super().__init__(Color.NEUTRAL, pos, is_tipped)

        self.classname = type(self).__name__


class BlueGoal(Goal, ISerializable):
    def __init__(self, pos, is_tipped=False):
        super().__init__(Color.BLUE, pos, is_tipped)

        self.classname = type(self).__name__


class Robot(ITippable, ISerializable):
    def __init__(self, color, pos, is_tipped=False):
        self.color = color
        self.rings = []
        self.goals = []
        self.position = pos
        self.is_tipped = is_tipped
        self.classname = type(self).__name__

    def get_position(self):
        return self.position

    def get_rings(self):
        return self.rings

    def add_goal(self, goal):
        self.goals.append(goal)

    def get_goals(self):
        return self.goals

    def is_tipped(self):
        return self.is_tipped


class HostRobot(Robot, ISerializable):
    def __init__(self, color, pos, is_tipped=False):
        super().__init__(color, pos, is_tipped)

        self.classname = type(self).__name__


class PartnerRobot(Robot, ISerializable):
    def __init__(self, color, pos, is_tipped=False):
        super().__init__(color, pos, is_tipped)

        self.classname = type(self).__name__


class OpposingRobot(Robot, ISerializable):
    def __init__(self, color, pos, is_tipped=False):
        super().__init__(color, pos, is_tipped)

        self.classname = type(self).__name__


@DeprecationWarning
class RedRobot(Robot, ISerializable):
    def __init__(self, pos, is_tipped=False):
        super().__init__(Color.RED, pos, is_tipped)

        self.classname = type(self).__name__


@DeprecationWarning
class BlueRobot(Robot, ISerializable):
    def __init__(self, pos, is_tipped=False):
        super().__init__(Color.BLUE, pos, is_tipped)

        self.classname = type(self).__name__


class Platform(IScorable, ISerializable):
    def __init__(self, color, state):
        self.color = color
        self.state = state
        self.rings = []
        self.goals = []
        self.robots = []
        self.classname = type(self).__name__

    def get_rings(self):
        return self.rings

    def add_goal(self, goal):
        self.goals.append(goal)

    def get_goals(self):
        return self.goals

    def add_robot(self, robot):
        self.robots.append(robot)

    def get_robots(self):
        return self.robots

    def get_current_score(self, color):
        if self.state == PlatformState.LEVEL:
            robots = list(filter(lambda rob: rob.color ==
                          color, self.get_robots()))
            goals = list(filter(lambda goal: goal.color ==
                                color, self.get_goals()))
            return (30 * len(robots)) + (40 * len(goals))
        else:
            return 0


class RedPlatform(Platform, ISerializable):
    def __init__(self, state=PlatformState.LEVEL):
        super().__init__(Color.RED, state)

        self.classname = type(self).__name__


class BluePlatform(Platform, ISerializable):
    def __init__(self, state=PlatformState.LEVEL):
        super().__init__(Color.BLUE, state)

        self.classname = type(self).__name__
