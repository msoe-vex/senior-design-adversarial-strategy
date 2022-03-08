from entities.classUtils import AbstractClass
from entities.interfaces import IScorable, ISerializable
from enum import Enum
from entities.enumerations import Color
from entities.scoring_elements import Ring, Goal
from entities.robots import Robot


class PlatformState(int, Enum):
    LEFT = 0
    RIGHT = 1
    LEVEL = 2


class Platform(AbstractClass, IScorable, ISerializable):
    def __init__(self, color: Color, state: PlatformState, rings: list[Ring]=[], goals: list[Goal]=[], robots: list[Robot]=[]):
        self.color = color
        self.state = state
        self.rings = rings
        self.goals = goals
        self.robots = robots

    def __get_current_score(self, color: Color):
        if self.state == PlatformState.LEVEL:
            robots = list(filter(lambda rob: rob.color == color, self.robots))
            goals = list(filter(lambda goal: goal.color == color or goal.color == Color.NEUTRAL, self.goals))
            return (30 * len(robots)) + (40 * len(goals))
        else:
            return 0


class RedPlatform(Platform, ISerializable):
    def __init__(self, state: PlatformState, **kwargs):
        super().__init__(Color.RED, state, **kwargs)

    def get_current_score(self):
        return self.__get_current_score(Color.RED)


class BluePlatform(Platform, ISerializable):
    def __init__(self, state: PlatformState, **kwargs):
        super().__init__(Color.BLUE, state, **kwargs)

    def get_current_score(self):
        return self.__get_current_score(Color.BLUE)
