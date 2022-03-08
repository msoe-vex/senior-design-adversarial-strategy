from enum import Enum
from entities.classUtils import AbstractClass
from entities.interfaces import ITippable, ISerializable
from entities.mathUtils import Pose2D
from entities.scoring_elements import Ring, Goal
from entities.enumerations import Color


class RobotID(int, Enum):
    SELF = 0,
    PARTNER = 1,
    OPPOSING = 2,


class Robot(AbstractClass, ITippable, ISerializable):
    def __init__(self, color: Color, id: RobotID, position: Pose2D, rings: list[Ring]=[], goals: list[Goal]=[], tipped: bool=False):
        self.color = color
        self.id = id
        self.position = position
        self.rings = rings
        self.goals = goals
        self.tipped = tipped

    def is_tipped(self) -> bool:
        return self.tipped


class HostRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, **kwargs):
        super().__init__(color, RobotID.SELF, pos, kwargs)


class PartnerRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, **kwargs):
        super().__init__(color, RobotID.PARTNER, pos, kwargs)


class OpposingRobot(Robot, ISerializable):
    def __init__(self, color: Color, pos: Pose2D, **kwargs):
        super().__init__(color, RobotID.OPPOSING, pos, kwargs)
