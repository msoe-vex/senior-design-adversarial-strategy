from enum import Enum
from typing import List
from dataclasses import field
from .classUtils import AbstractDataClass, nested_dataclass
from .interfaces import IScorable, ISerializable
from .enumerations import Color
from .scoring_elements import Ring, Goal
from .robots import Robot


class PlatformState(int, Enum):
    LEFT = 0
    RIGHT = 1
    LEVEL = 2


@nested_dataclass
class Platform(AbstractDataClass, IScorable, ISerializable):
    color: Color
    state: PlatformState
    rings: List[Ring] = field(default_factory=list)
    goals: List[Goal] = field(default_factory=list)
    robots: List[Robot] = field(default_factory=list)

    def __get_current_score(self, color: Color):
        if self.state == PlatformState.LEVEL:
            robots = list(filter(lambda rob: rob.color == color, self.robots))
            goals = list(
                filter(
                    lambda goal: goal.color == color or goal.color == Color.NEUTRAL,
                    self.goals,
                )
            )
            return (30 * len(robots)) + (40 * len(goals))
        else:
            return 0


@nested_dataclass
class RedPlatform(Platform, ISerializable):
    def __init__(self, state: PlatformState, **kwargs):
        super().__init__(Color.RED, state, **kwargs)

    def get_current_score(self):
        return self.__get_current_score(Color.RED)


@nested_dataclass
class BluePlatform(Platform, ISerializable):
    def __init__(self, state: PlatformState, **kwargs):
        super().__init__(Color.BLUE, state, **kwargs)

    def get_current_score(self):
        return self.__get_current_score(Color.BLUE)
