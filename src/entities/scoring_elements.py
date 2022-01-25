from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from entities.math_utils import Pose2D
from enum import Enum
from entities.interfaces import ITippable, IScorable, ISerializable
from entities.class_utils import AbstractDataClass
from entities.enumerations import Color


class GoalLevel(int, Enum):
    BASE = 1
    LOW = 3
    HIGH = 10


@dataclass
class Ring(ISerializable):
    position: Pose2D


@dataclass
class RingContainer(ISerializable):
    max_storage: int = 8
    rings: List[Ring] = field(default_factory=list)

    def add_ring(self, ring: Ring) -> None:
        self.rings.append(ring)

    def get_utilization(self) -> int:
        return len(self.rings)

    def get_remaining_utilization(self) -> int:
        return self.max_storage - self.get_utilization()


@dataclass
class Goal(AbstractDataClass, ITippable, IScorable, ISerializable):
    color: Color = Color.NEUTRAL
    position: Pose2D = Pose2D(0, 0)
    ring_containers: dict[GoalLevel, RingContainer] = field(default_factory=dict)
    tipped: bool = False
    current_zone: Color = field(init=False)

    def __post_init__(self):
        if self.position.y <= 48:
            self.current_zone = Color.RED
        elif self.position.y >= 96:
            self.current_zone = Color.BLUE
        else:
            self.current_zone = Color.NEUTRAL

    def is_tipped(self) -> bool:
        return self.tipped

    def get_ring_container(self, level: GoalLevel) -> RingContainer:
        return self.ring_containers[level]

    def get_ring_score(self) -> int:
        score = 0
        for level in self.ring_containers:
            score += level.value * self.get_ring_container(level).get_utilization()
        return score

    def get_current_score(self, color: Color) -> int:
        if self.current_zone == color or self.color == Color.NEUTRAL:
            return 20 + self.get_ring_score()
        else:
            return 0


@dataclass
class RedGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.RED, pos, kwargs)


@dataclass
class NeutralGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.NEUTRAL, pos, kwargs)


@dataclass
class BlueGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.BLUE, pos, kwargs)
