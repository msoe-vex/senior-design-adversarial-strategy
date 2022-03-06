from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from entities.math_utils import Pose2D
from enum import Enum
from entities.interfaces import ITippable, IScorable, ISerializable
from entities.class_utils import AbstractDataClass
from entities.enumerations import Color, GoalLevel


@dataclass
class Ring(ISerializable):
    position: Pose2D


@dataclass
class RingContainer(ISerializable):
    max_storage: int = 8
    rings: List[Ring] = field(default_factory=list)

    def add_ring(self, ring: Ring) -> bool:
        if self.get_remaining_utilization() > 0:
            self.rings.append(ring)
            return True
        return False

    def add_rings(self, rings: List[Ring]) -> bool:
        if self.get_remaining_utilization() > len(rings):
            self.rings = self.rings + rings
            return True
        return False

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
        return 0

    def add_ring(self, ring: Ring, level: GoalLevel) -> bool:
        if self.get_ring_container(level).get_remaining_utilization() > 0:
            self.get_ring_container(level).add_ring(ring)
            return True
        return False


@dataclass
class RedGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.RED, pos, kwargs)

        self.ring_containers[GoalLevel.BASE] = RingContainer()
        self.ring_containers[GoalLevel.LOW] = RingContainer()
        self.ring_containers[GoalLevel.HIGH] = RingContainer(0)


@dataclass
class BlueGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.BLUE, pos, kwargs)

        self.ring_containers[GoalLevel.BASE] = RingContainer()
        self.ring_containers[GoalLevel.LOW] = RingContainer()
        self.ring_containers[GoalLevel.HIGH] = RingContainer(0)


@dataclass
class HighNeutralGoal(Goal, ISerializable):
    level: GoalLevel = GoalLevel.HIGH

    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.NEUTRAL, pos, kwargs)

        self.ring_containers[GoalLevel.BASE] = RingContainer()
        self.ring_containers[GoalLevel.LOW] = RingContainer()
        self.ring_containers[GoalLevel.HIGH] = RingContainer()


@dataclass
class LowNeutralGoal(Goal, ISerializable):
    level: GoalLevel = GoalLevel.LOW

    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.NEUTRAL, pos, kwargs)

        self.ring_containers[GoalLevel.BASE] = RingContainer()
        self.ring_containers[GoalLevel.LOW] = RingContainer()
        self.ring_containers[GoalLevel.HIGH] = RingContainer(0)