from __future__ import annotations
from typing import List
from entities.mathUtils import Pose2D
from entities.interfaces import ITippable, IScorable, ISerializable
from entities.classUtils import AbstractClass
from entities.enumerations import Color, GoalLevel


class Ring(ISerializable):
    def __init__(self, position: Pose2D):
        self.position = position


class RingContainer(ISerializable):
    def __init__(self, max_storage: int=8, rings: list[Ring]=[]):
        self.max_storage = max_storage
        self.rings = rings

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


class Goal(AbstractClass, ITippable, IScorable, ISerializable):
    def __init__(self, color: Color, position: Pose2D, ring_containers: dict[GoalLevel, RingContainer]={}, tipped: bool=False):
        self.color = color
        self.position = position
        self.ring_containers = ring_containers
        self.tipped = tipped
        
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


class RedGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.RED, pos, kwargs)

        self.ring_containers[GoalLevel.BASE] = RingContainer()
        self.ring_containers[GoalLevel.LOW] = RingContainer()
        self.ring_containers[GoalLevel.HIGH] = RingContainer(0)


class BlueGoal(Goal, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.BLUE, pos, kwargs)

        self.ring_containers[GoalLevel.BASE] = RingContainer()
        self.ring_containers[GoalLevel.LOW] = RingContainer()
        self.ring_containers[GoalLevel.HIGH] = RingContainer(0)


class HighNeutralGoal(Goal, ISerializable):
    level: GoalLevel = GoalLevel.HIGH

    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.NEUTRAL, pos, kwargs)

        self.ring_containers[GoalLevel.BASE] = RingContainer()
        self.ring_containers[GoalLevel.LOW] = RingContainer()
        self.ring_containers[GoalLevel.HIGH] = RingContainer()


class LowNeutralGoal(Goal, ISerializable):
    level: GoalLevel = GoalLevel.LOW

    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.NEUTRAL, pos, kwargs)

        self.ring_containers[GoalLevel.BASE] = RingContainer()
        self.ring_containers[GoalLevel.LOW] = RingContainer()
        self.ring_containers[GoalLevel.HIGH] = RingContainer(0)