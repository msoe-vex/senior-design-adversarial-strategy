from field import Field, FieldState
from game_objects import Platform, RedPlatform, BluePlatform, Ring, RedGoal, NeutralGoal, BlueGoal, HostRobot, PartnerRobot, OpposingRobot, Color, GoalLevel, PlatformState
from mapping import Pose2D


def basic_goal_representation():
    goalArr = [
        RedGoal(Pose2D(55, 35)),
        RedGoal(Pose2D(-50, 10)),
        BlueGoal(Pose2D(-55, 105)),
        BlueGoal(Pose2D(50, 134)),
        NeutralGoal(Pose2D(-48, 72)),
        NeutralGoal(Pose2D(0, 72)),
        NeutralGoal(Pose2D(48, 72))
    ]

    robotArr = [
        HostRobot(Color.RED, Pose2D(30, 0)),
        PartnerRobot(Color.RED, Pose2D(-30, 0)),
        OpposingRobot(Color.BLUE, Pose2D(30, 144)),
        OpposingRobot(Color.BLUE, Pose2D(-30, 144))
    ]

    return Field(goals=goalArr, robots=robotArr)

