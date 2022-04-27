from enum import Enum
from typing import List
from dataclasses import field
from .constants import FIELD_WIDTH_IN, PLATFORM_LENGTH_IN, PLATFORM_WIDTH_IN
from .mathUtils import Pose2D
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

            robot_goals = []
            for robot in self.robots:
                if robot.check_front_goal():
                    robot_goals.append(robot.front_goal)

                if robot.check_rear_goal():
                    robot_goals.append(robot.rear_goal)

            goals = list(
                filter(
                    lambda goal: goal.color == color or goal.color == Color.NEUTRAL,
                    self.goals + robot_goals,
                )
            )
            return (30 * len(robots)) + (40 * len(goals))
        else:
            return 0

    def is_colliding(self, pose: Pose2D) -> bool:
        """
        Return True if the given pose collides with the ramps
        """
        if self.color == Color.RED:
            return pose.x > (0 - (PLATFORM_LENGTH_IN / 2)) and pose.x < (PLATFORM_LENGTH_IN / 2) and \
                pose.y < PLATFORM_WIDTH_IN
        return pose.x > (0 - (PLATFORM_LENGTH_IN / 2)) and pose.x < (PLATFORM_LENGTH_IN / 2) and \
                pose.y > (FIELD_WIDTH_IN- PLATFORM_WIDTH_IN)


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
