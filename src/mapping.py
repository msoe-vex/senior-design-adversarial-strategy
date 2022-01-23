import math
from serialization import ISerializable


def distanceBetweenPoints(p1, p2):
    return p1.distTo(p2)


class Pose2D(ISerializable):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.classname = type(self).__name__

    def distTo(self, pose):
        x_dist = (pose.x - self.x) ** 2
        y_dist = (pose.y - self.y) ** 2
        return math.sqrt(x_dist + y_dist)


