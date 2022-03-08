from dataclasses import field
from enum import Enum
from entities.classUtils import AbstractDataClass, nested_dataclass
from entities.interfaces import ITippable, ISerializable
from entities.mathUtils import Pose2D
from entities.scoring_elements import Ring, Goal
from entities.enumerations import Color


class RobotID(int, Enum):
    SELF = (0,)
    PARTNER = (1,)
    OPPOSING = (2,)


@nested_dataclass
class Robot(AbstractDataClass, ITippable, ISerializable):
    color: Color = Color.RED
    id: RobotID = RobotID.SELF
    position: Pose2D = Pose2D(0, 0)
    rings: list[Ring] = field(default_factory=list)
    goals: list[Goal] = field(default_factory=list)
    tipped: bool = False

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
