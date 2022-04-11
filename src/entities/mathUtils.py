from __future__ import annotations
import math

from .classUtils import nested_dataclass
from .interfaces import ISerializable


class Pose2D(ISerializable):
    """
    A position within a 2D coordinate frame

    @param x: X-Coordinate of the position
    @param y: Y-Coordinate of the position
    @param angle: Angle of the position, in radians, mapping to a unit circle
    """
    def __init__(self, x: float, y: float, angle: float):
        self.x = x
        self.y = y
        self.angle = angle

    def distTo(self, pose: Pose2D) -> float:
        x_dist = (pose.x - self.x) ** 2
        y_dist = (pose.y - self.y) ** 2
        return math.sqrt(x_dist + y_dist)


class ICollisionsEnabled:
    """
    Due to bad inheritance logic, classes that implement this interface require their own instances of pose and radius to be instantiated (with the same names) for this to work.
    """
    pose: Pose2D = Pose2D(0, 0, 0)
    radius: float = 0.

    def __init__(self):
        # Empty to allow for child class constructor to work in multiple inheritance
        # This can be fixed by modifying the class decorator to propagate the method resolution order
        # https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
        pass

    def is_colliding(self, other_obj: "ICollisionsEnabled"):
        return other_obj.pose.distTo(self.pose) < max(self.radius, other_obj.radius)

    def is_colliding_front(self, other_obj: "ICollisionsEnabled", collision_radius: float):
        # Get point in front of the object, on the radius circle
        # Since our angles are based on the positive x-axis, start the point on the radius of the object, on the positive x-axis side
        new_x = ((self.pose.x + self.radius) * math.cos(self.pose.angle)) - (self.pose.y * math.sin(self.pose.angle))
        new_y = ((self.pose.x + self.radius) * math.sin(self.pose.angle)) - (self.pose.y * math.cos(self.pose.angle))
        front_point = Pose2D(new_x, new_y, self.pose.angle)

        return other_obj.pose.distTo(front_point) <= collision_radius

    def is_colliding_rear(self, other_obj: "ICollisionsEnabled", collision_radius: float):
        # Get point behind the current object, on the radius circle
        # Since our angles are based on the positive x-axis, start the point on the radius of the object, on the positive x-axis side
        rear_angle = self.pose.angle + math.pi
        new_x = ((self.pose.x + self.radius) * math.cos(rear_angle)) - (self.pose.y * math.sin(rear_angle))
        new_y = ((self.pose.x + self.radius) * math.sin(rear_angle)) - (self.pose.y * math.cos(rear_angle))
        rear_point = Pose2D(new_x, new_y, self.pose.angle)

        return other_obj.pose.distTo(rear_point) <= collision_radius


def distance_between_points(p1: Pose2D, p2: Pose2D) -> float:
    return p1.distTo(p2)
