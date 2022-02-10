from dataclasses import dataclass, field
from enum import Enum
from typing import List
from entities.class_utils import AbstractDataClass
from entities.interfaces import ITippable, ISerializable
from entities.math_utils import Pose2D
from entities.scoring_elements import Ring, Goal
from entities.enumerations import Color


class RobotID(int, Enum):
    SELF = 0,
    PARTNER = 1,
    OPPOSING = 2,


@dataclass
class Robot(AbstractDataClass, ITippable, ISerializable):
    color: Color = Color.RED
    id: RobotID = RobotID.SELF
    position: Pose2D = Pose2D(0, 0)
    rings: List[Ring] = field(default_factory=list)
    goals: List[Goal] = field(default_factory=list)
    tipped: bool = False

    def is_tipped(self) -> bool:
        return self.tipped


@dataclass
class HostRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, **kwargs):
        super().__init__(color, RobotID.SELF, pos, kwargs)


@dataclass
class PartnerRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, **kwargs):
        super().__init__(color, RobotID.PARTNER, pos, kwargs)


@dataclass
class OpposingRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, **kwargs):
        super().__init__(color, RobotID.OPPOSING, pos, kwargs)


@DeprecationWarning
@dataclass
class RedRobot(Robot, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.RED, pos, kwargs)


@DeprecationWarning
@dataclass
class BlueRobot(Robot, ISerializable):
    def __init__(self, pos: Pose2D, **kwargs):
        super().__init__(Color.BLUE, pos, kwargs)
