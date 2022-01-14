from typing import List
from entities.class_utils import AbstractDataClass
from entities.interfaces import IScorable, ISerializable
from enum import Enum
from dataclasses import dataclass, field
from entities.enumerations import Color
from entities.scoring_elements import Ring, Goal
from entities.robots import Robot


class PlatformState(str, Enum):
    LEFT = 1
    RIGHT = 2
    LEVEL = 3


@dataclass
class Platform(AbstractDataClass, IScorable, ISerializable):
    color: Color = Color.RED
    state: PlatformState = PlatformState.LEVEL
    rings: List[Ring] = field(default_factory=list)
    goals: List[Goal] = field(default_factory=list)
    robots: List[Robot] = field(default_factory=list)

    def get_current_score(self, color: Color):
        if self.state == PlatformState.LEVEL:
            robots = list(filter(lambda rob: rob.color == color, self.get_robots()))
            goals = list(filter(lambda goal: goal.color == color, self.get_goals()))
            return (30 * len(robots)) + (40 * len(goals))
        else:
            return 0


@dataclass
class RedPlatform(Platform, ISerializable):
    def __init__(self, state: PlatformState = PlatformState.LEVEL, **kwargs):
        super().__init__(Color.RED, state, kwargs)


@dataclass
class BluePlatform(Platform, ISerializable):
    def __init__(self, state: PlatformState = PlatformState.LEVEL, **kwargs):
        super().__init__(Color.BLUE, state, kwargs)
