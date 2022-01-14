from entities.field import Field
from entities.scoring_elements import RedGoal, NeutralGoal, BlueGoal
from entities.robots import HostRobot, PartnerRobot, OpposingRobot
from entities.math_utils import Pose2D
from entities.enumerations import Color


def basic_goal_representation():
    goalArr = [
        RedGoal(Pose2D(55, 35)),
        RedGoal(Pose2D(-50, 10)),
        BlueGoal(Pose2D(-55, 105)),
        BlueGoal(Pose2D(50, 134)),
        NeutralGoal(Pose2D(-48, 72)),
        NeutralGoal(Pose2D(0, 72)),
        NeutralGoal(Pose2D(48, 72)),
    ]

    robotArr = [
        HostRobot(Color.RED, Pose2D(30, 0)),
        PartnerRobot(Color.RED, Pose2D(-30, 0)),
        OpposingRobot(Color.BLUE, Pose2D(30, 144)),
        OpposingRobot(Color.BLUE, Pose2D(-30, 144)),
    ]

    return Field(goals=goalArr, robots=robotArr)
