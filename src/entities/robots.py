from dataclasses import dataclass, field
from typing import List
from entities.class_utils import AbstractDataClass
from entities.interfaces import ITippable, ISerializable
from entities.math_utils import Pose2D
from entities.scoring_elements import Ring, Goal
from entities.enumerations import Color


@dataclass
class Robot(AbstractDataClass, ITippable, ISerializable):
    color: Color = Color.RED
    position: Pose2D = Pose2D(0, 0)
    rings: List[Ring] = field(default_factory=list)
    goals: List[Goal] = field(default_factory=list)
    tipped: bool = False
    classname: str = field(init=False)

    def __post_init__(self):
        self.classname = type(self).__name__

    def is_tipped(self) -> bool:
        return self.tipped


@dataclass
class HostRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, tipped: bool = False):
        super().__init__(color, pos, tipped)

        self.classname = type(self).__name__


@dataclass
class PartnerRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, tipped: bool = False):
        super().__init__(color, pos, tipped)

        self.classname = type(self).__name__


@dataclass
class OpposingRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, tipped: bool = False):
        super().__init__(color, pos, tipped)

        self.classname = type(self).__name__


@DeprecationWarning
@dataclass
class RedRobot(Robot, ISerializable):
    def __init__(self, pos: Pose2D, tipped: bool = False):
        super().__init__(Color.RED, pos, tipped)

        self.classname = type(self).__name__


@DeprecationWarning
@dataclass
class BlueRobot(Robot, ISerializable):
    def __init__(self, pos: Pose2D, tipped: bool = False):
        super().__init__(Color.BLUE, pos, tipped)

        self.classname = type(self).__name__
