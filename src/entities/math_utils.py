from dataclasses import dataclass, field
import math
from entities.interfaces import ISerializable
from dataclasses import dataclass


@dataclass
class Pose2D(ISerializable):
    x: float
    y: float

    def distTo(self, pose: "Pose2D") -> float:
        x_dist = (pose.x - self.x) ** 2
        y_dist = (pose.y - self.y) ** 2
        return math.sqrt(x_dist + y_dist)


def distanceBetweenPoints(p1: Pose2D, p2: Pose2D) -> float:
    return p1.distTo(p2)
