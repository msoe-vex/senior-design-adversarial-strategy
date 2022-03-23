from __future__ import annotations
import math
from entities.interfaces import ISerializable


class Pose2D(ISerializable):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distTo(self, pose: Pose2D) -> float:
        x_dist = (pose.x - self.x) ** 2
        y_dist = (pose.y - self.y) ** 2
        return math.sqrt(x_dist + y_dist)


class ICollisionsEnabled:
    pose: Pose2D = Pose2D(0, 0)
    radius: float = 0.

    def is_colliding(self, other_obj: "ICollisionsEnabled"):
        return other_obj.pose.distTo(self.pose) < max(self.radius, other_obj.radius)


def distance_between_points(p1: Pose2D, p2: Pose2D) -> float:
    return p1.distTo(p2)
