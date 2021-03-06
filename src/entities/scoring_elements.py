from __future__ import annotations
from dataclasses import field
from logging import getLogger
from typing import List
from .constants import REPRESENTATION_LOGGER_NAME
from .mathUtils import Pose2D, ICollisionsEnabled
from .interfaces import ITippable, IScorable, ISerializable
from .classUtils import AbstractDataClass, nested_dataclass
from .enumerations import Color, GoalLevel
from .constants import GOAL_RADIUS, RING_RADIUS


@nested_dataclass
class Ring(ICollisionsEnabled, ISerializable):
    pose: Pose2D
    radius: float = RING_RADIUS


@nested_dataclass
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


@nested_dataclass
class Goal(AbstractDataClass, ITippable, IScorable, ICollisionsEnabled, ISerializable):
    color: Color = Color.NEUTRAL
    pose: Pose2D = Pose2D(0, 0, 0)
    level: GoalLevel = GoalLevel.LOW
    ring_containers: dict[GoalLevel, RingContainer] = field(default_factory=dict)
    tipped: bool = False
    radius: float = GOAL_RADIUS

    def is_tipped(self) -> bool:
        return self.tipped

    def get_ring_container(self, level: GoalLevel) -> RingContainer:
        return self.ring_containers[level]

    def get_total_rings(self) -> int:
        total = 0

        for level in self.ring_containers:
            total += self.get_ring_container(level).get_utilization()

        return total

    def get_ring_score(self) -> int:
        score = 0
        for level in self.ring_containers:
            score += level.value * self.get_ring_container(level).get_utilization()
        return score

    def get_current_zone(self) -> Color:
        if self.pose.y <= 48:
            return Color.RED
        elif self.pose.y >= 96:
            return Color.BLUE
        else:
            return Color.NEUTRAL

    def get_current_score(self, color: Color) -> int:
        if self.get_current_zone() == color and (
            self.color == color or self.color == Color.NEUTRAL
        ):
            return 20 + self.get_ring_score()
        return 0

    def add_ring(self, ring: Ring, level: GoalLevel) -> bool:
        if self.get_ring_container(level).get_remaining_utilization() > 0:
            self.get_ring_container(level).add_ring(ring)
            return True
        return False


@nested_dataclass
class RedGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.RED, pos, **kwargs)

        if not self.ring_containers.get(GoalLevel.BASE, None):
            self.ring_containers[GoalLevel.BASE] = RingContainer()

        if not self.ring_containers.get(GoalLevel.LOW, None):
            self.ring_containers[GoalLevel.LOW] = RingContainer()

        if self.ring_containers.get(GoalLevel.HIGH, None):
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Error in RedGoal initialization: Rings placed on non-existent high branch"
            )

        self.ring_containers[GoalLevel.HIGH] = RingContainer(0)


@nested_dataclass
class BlueGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.BLUE, pos, **kwargs)

        if not self.ring_containers.get(GoalLevel.BASE, None):
            self.ring_containers[GoalLevel.BASE] = RingContainer()

        if not self.ring_containers.get(GoalLevel.LOW, None):
            self.ring_containers[GoalLevel.LOW] = RingContainer()

        if self.ring_containers.get(GoalLevel.HIGH, None):
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Error in BlueGoal initialization: Rings placed on non-existent high branch"
            )

        self.ring_containers[GoalLevel.HIGH] = RingContainer(0)


@nested_dataclass
class HighNeutralGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.NEUTRAL, pos, level=GoalLevel.HIGH, **kwargs)

        if not self.ring_containers.get(GoalLevel.BASE, None):
            self.ring_containers[GoalLevel.BASE] = RingContainer()

        if not self.ring_containers.get(GoalLevel.LOW, None):
            self.ring_containers[GoalLevel.LOW] = RingContainer()

        if not self.ring_containers.get(GoalLevel.HIGH, None):
            self.ring_containers[GoalLevel.HIGH] = RingContainer()


@nested_dataclass
class LowNeutralGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.NEUTRAL, pos, **kwargs)

        if not self.ring_containers.get(GoalLevel.BASE, None):
            self.ring_containers[GoalLevel.BASE] = RingContainer()

        if not self.ring_containers.get(GoalLevel.LOW, None):
            self.ring_containers[GoalLevel.LOW] = RingContainer()

        if self.ring_containers.get(GoalLevel.HIGH, None):
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Error in LowNeutralGoal initialization: Rings placed on non-existent high branch"
            )

        self.ring_containers[GoalLevel.HIGH] = RingContainer(0)
