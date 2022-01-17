from entities.field import Field
from entities.platforms import BluePlatform, PlatformState, RedPlatform
from entities.scoring_elements import GoalLevel, RedGoal, NeutralGoal, BlueGoal, Ring, RingContainer
from entities.robots import HostRobot, PartnerRobot, OpposingRobot
from entities.math_utils import Pose2D
from entities.enumerations import Color


def basic_goal_representation():
    goal_arr = [
        RedGoal(Pose2D(60, 35)), # Bottom Red
        RedGoal(Pose2D(-30, 10)), # Top Red
        BlueGoal(Pose2D(-60, 109)), # Top Blue
        BlueGoal(Pose2D(30, 134)), # Bottom Blue
        NeutralGoal(Pose2D(-35, 72)), # Top Neutral
        NeutralGoal(Pose2D(0, 72)), # Mid Neutral
        NeutralGoal(Pose2D(35, 72)), # Bottom Neutral
    ]

    robot_arr = [
        HostRobot(Color.RED, Pose2D(30, 0)), # Bottom Red
        PartnerRobot(Color.RED, Pose2D(-30, 0)), # Top Red
        OpposingRobot(Color.BLUE, Pose2D(30, 144)), # Bottom Blue
        OpposingRobot(Color.BLUE, Pose2D(-30, 144)), # Top Blue
    ]

    return Field(goals=goal_arr, robots=robot_arr)

def basic_ring_representation():
    ring_arr = [
        Ring(Pose2D(-69, 72)), # Top L
        Ring(Pose2D(-62, 72)),
        Ring(Pose2D(-55, 72)),
        Ring(Pose2D(-48, 72)),
        Ring(Pose2D(-48, 78)),
        Ring(Pose2D(-48, 84)),
        Ring(Pose2D(-48, 90)),
        Ring(Pose2D(-48, 96)),
        Ring(Pose2D(-25, 72)), # Top-Mid Line
        Ring(Pose2D(-17, 72)),
        Ring(Pose2D(-9, 72)),
        Ring(Pose2D(9, 72)), # Bottom-Mid Line
        Ring(Pose2D(17, 72)),
        Ring(Pose2D(25, 72)),
        Ring(Pose2D(69, 72)), # Bottom L
        Ring(Pose2D(62, 72)),
        Ring(Pose2D(55, 72)),
        Ring(Pose2D(48, 72)),
        Ring(Pose2D(48, 66)),
        Ring(Pose2D(48, 60)),
        Ring(Pose2D(48, 54)),
        Ring(Pose2D(48, 48)), 
    ]

    robot_arr = [
        HostRobot(Color.RED, Pose2D(30, 0)), # Bottom Red
        PartnerRobot(Color.RED, Pose2D(-30, 0)), # Top Red
        OpposingRobot(Color.BLUE, Pose2D(30, 144)), # Bottom Blue
        OpposingRobot(Color.BLUE, Pose2D(-30, 144)), # Top Blue
    ]

    return Field(rings=ring_arr, robots=robot_arr)

def starting_representation():
    ring_arr = [
        Ring(Pose2D(-69, 72)), # Top L
        Ring(Pose2D(-62, 72)),
        Ring(Pose2D(-55, 72)),
        Ring(Pose2D(-48, 72)),
        Ring(Pose2D(-48, 78)),
        Ring(Pose2D(-48, 84)),
        Ring(Pose2D(-48, 90)),
        Ring(Pose2D(-48, 96)),
        Ring(Pose2D(-25, 72)), # Top-Mid Line
        Ring(Pose2D(-17, 72)),
        Ring(Pose2D(-9, 72)),
        Ring(Pose2D(9, 72)), # Bottom-Mid Line
        Ring(Pose2D(17, 72)),
        Ring(Pose2D(25, 72)),
        Ring(Pose2D(69, 72)), # Bottom L
        Ring(Pose2D(62, 72)),
        Ring(Pose2D(55, 72)),
        Ring(Pose2D(48, 72)),
        Ring(Pose2D(48, 66)),
        Ring(Pose2D(48, 60)),
        Ring(Pose2D(48, 54)),
        Ring(Pose2D(48, 48)), 
        Ring(Pose2D(-28, 48)),# Left Top Star
        Ring(Pose2D(-25, 45)),
        Ring(Pose2D(-25, 48)),
        Ring(Pose2D(-25, 51)),
        Ring(Pose2D(-22, 48)),
        Ring(Pose2D(-3, 48)), # Left Bottom Star
        Ring(Pose2D(0, 45)),
        Ring(Pose2D(0, 48)),
        Ring(Pose2D(0, 51)),
        Ring(Pose2D(3, 48)),
        Ring(Pose2D(-3, 95)), # Right Top Star
        Ring(Pose2D(0, 92)),
        Ring(Pose2D(0, 95)),
        Ring(Pose2D(0, 98)),
        Ring(Pose2D(3, 95)),
        Ring(Pose2D(22, 95)), # Right Bottom Star
        Ring(Pose2D(25, 92)),
        Ring(Pose2D(25, 95)),
        Ring(Pose2D(25, 98)),
        Ring(Pose2D(28, 95)),
    ]
    
    goal_arr = [
        RedGoal(Pose2D(60, 35)), # Bottom Red
        RedGoal(Pose2D(-30, 10)), # Top Red
        BlueGoal(Pose2D(-60, 109)), # Top Blue
        BlueGoal(Pose2D(30, 134)), # Bottom Blue
        NeutralGoal(Pose2D(-35, 72)), # Top Neutral
        NeutralGoal(Pose2D(0, 72)), # Mid Neutral
        NeutralGoal(Pose2D(35, 72)), # Bottom Neutral
    ]

    red_plat = RedPlatform(PlatformState.LEFT)

    blue_plat = BluePlatform(PlatformState.RIGHT)

    robot_arr = [
        HostRobot(Color.RED, Pose2D(30, 0)), # Bottom Red
        PartnerRobot(Color.RED, Pose2D(-30, 0)), # Top Red
        OpposingRobot(Color.BLUE, Pose2D(30, 144)), # Bottom Blue
        OpposingRobot(Color.BLUE, Pose2D(-30, 144)), # Top Blue
    ]

    return Field(rings=ring_arr, goals=goal_arr, red_platform=red_plat, blue_platform=blue_plat, robots=robot_arr)

def ending_representation():
    ring_arr = [
        Ring(Pose2D(-69, 25)),
        Ring(Pose2D(-62, 121)),
        Ring(Pose2D(-55, 32)),
        Ring(Pose2D(-44, 96)),
        Ring(Pose2D(-25, 22)),
        Ring(Pose2D(-17, 7)),
        Ring(Pose2D(9, 72)), 
        Ring(Pose2D(19, 61)), 
        Ring(Pose2D(6, 99)),
        Ring(Pose2D(48, 84)),
        Ring(Pose2D(-28, 48)),
        Ring(Pose2D(-25, 4)),
        Ring(Pose2D(-22, 48)),
        Ring(Pose2D(-3, 22)), 
        Ring(Pose2D(26, 45)),
        Ring(Pose2D(0, 14)),
        Ring(Pose2D(0, 51)),
        Ring(Pose2D(23, 100)),
        Ring(Pose2D(-3, 95)), 
        Ring(Pose2D(32, 104)),
        Ring(Pose2D(22, 95)), 
        Ring(Pose2D(8, 95))
    ]
    
    goal_arr = [
        RedGoal(
            Pose2D(25, -63), 
            ring_containers={
                GoalLevel.BASE: RingContainer(
                    rings = [
                        Ring(Pose2D(25, -63)),
                        Ring(Pose2D(25, -63))
                    ]
                ),
                GoalLevel.LOW: RingContainer(
                    rings = [
                        Ring(Pose2D(25, -63)),
                        Ring(Pose2D(25, -63)),
                        Ring(Pose2D(25, -63))
                    ]
                )
            }
        ),
        RedGoal(
            Pose2D(-49, 18),
            ring_containers={
                GoalLevel.BASE: RingContainer(
                    rings = [
                        Ring(Pose2D(-49, 18))
                    ]
                )
            }
        ),
        NeutralGoal(
            Pose2D(-21, 38),
            ring_containers={
                GoalLevel.BASE: RingContainer(
                    rings = [
                        Ring(Pose2D(-21, 38)),
                        Ring(Pose2D(-21, 38))
                    ]
                ),
                GoalLevel.LOW: RingContainer(
                    rings = [
                        Ring(Pose2D(-21, 38)),
                        Ring(Pose2D(-21, 38)),
                        Ring(Pose2D(-21, 38)),
                        Ring(Pose2D(-21, 38))
                    ]
                )
            }
        ), 
        NeutralGoal(
            Pose2D(0, 72), 
            tipped=True
        )
    ]

    red_plat = RedPlatform(
        PlatformState.LEVEL,
        robots = [
            HostRobot(
                Color.RED, 
                Pose2D(0, 4), 
                rings=[
                    Ring(Pose2D(0, 4)),
                    Ring(Pose2D(0, 4)),
                    Ring(Pose2D(0, 4))
                ], 
                goals=[
                    NeutralGoal(
                        Pose2D(0, 4),
                        ring_containers={
                            GoalLevel.HIGH: RingContainer(
                                rings = [
                                    Ring(Pose2D(0, 4)),
                                    Ring(Pose2D(0, 4)),
                                    Ring(Pose2D(0, 4)),
                                    Ring(Pose2D(0, 4)),
                                    Ring(Pose2D(0, 4))
                                ]
                            )
                        }
                    )
                ]
            )
        ]
    )

    blue_plat = BluePlatform(
        PlatformState.LEVEL,
        goals = [
            BlueGoal(
                Pose2D(0, 141),
                ring_containers={
                    GoalLevel.LOW: RingContainer(
                        rings = [
                            Ring(Pose2D(0, 141)),
                            Ring(Pose2D(0, 141)),
                            Ring(Pose2D(0, 141)),
                            Ring(Pose2D(0, 141)),
                            Ring(Pose2D(0, 141))
                        ]
                    )
                }
            ), 
        ],
        robots = [
            OpposingRobot(
                Color.BLUE, 
                Pose2D(-10, 142)
            ),
            OpposingRobot(
                Color.BLUE, 
                Pose2D(14, 141),
                goals = [
                    BlueGoal(
                        Pose2D(14, 141)
                    )
                ]
            )
        ]
    )

    robot_arr = [
        PartnerRobot(
            Color.RED, 
            Pose2D(-49, 71),
            tipped=True
        )
    ]

    return Field(rings=ring_arr, goals=goal_arr, red_platform=red_plat, blue_platform=blue_plat, robots=robot_arr)