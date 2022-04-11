from dataclasses import field
from enum import Enum
from typing import List
from .classUtils import AbstractDataClass, nested_dataclass
from .interfaces import ITippable, ISerializable
from .mathUtils import Pose2D, ICollisionsEnabled
from .scoring_elements import Ring, Goal
from .enumerations import Color
from .constants import ROBOT_RADIUS


class RobotID(int, Enum):
    SELF = 0
    PARTNER = 1
    OPPOSING = 2


@nested_dataclass
class Robot(AbstractDataClass, ITippable, ICollisionsEnabled, ISerializable):
    color: Color = Color.RED
    id: RobotID = RobotID.SELF
    pose: Pose2D = Pose2D(0, 0, 0)
    rings: List[Ring] = field(default_factory=list)
    goals: List[Goal] = field(default_factory=list)
    tipped: bool = False
    radius: float = ROBOT_RADIUS

    def is_tipped(self) -> bool:
        return self.tipped


@nested_dataclass
class HostRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, **kwargs):
        super().__init__(color, RobotID.SELF, pos, **kwargs)


@nested_dataclass
class PartnerRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, **kwargs):
        super().__init__(color, RobotID.PARTNER, pos, **kwargs)


@nested_dataclass
class OpposingRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, **kwargs):
        super().__init__(color, RobotID.OPPOSING, pos, **kwargs)
