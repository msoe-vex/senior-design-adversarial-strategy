from .fieldRepresentation import FieldRepresentation
from .platforms import BluePlatform, PlatformState, RedPlatform
from .scoring_elements import (
    GoalLevel,
    HighNeutralGoal,
    LowNeutralGoal,
    RedGoal,
    BlueGoal,
    Ring,
    RingContainer,
)
from .robots import HostRobot, PartnerRobot, OpposingRobot
from .mathUtils import Pose2D
from .enumerations import Color


def basic_goal_representation():
    goal_arr = [
        RedGoal(Pose2D(60, 35, 0)),  # Bottom Red
        RedGoal(Pose2D(-30, 10, 0)),  # Top Red
        BlueGoal(Pose2D(-60, 109, 0)),  # Top Blue
        BlueGoal(Pose2D(30, 134, 0)),  # Bottom Blue
        LowNeutralGoal(Pose2D(-35, 72, 0)),  # Top Neutral
        HighNeutralGoal(Pose2D(0, 72, 0)),  # Mid Neutral
        LowNeutralGoal(Pose2D(35, 72, 0)),  # Bottom Neutral
    ]

    robot_arr = [
        HostRobot(Color.RED, Pose2D(30, 0, 0)),  # Bottom Red
        PartnerRobot(Color.RED, Pose2D(-30, 0, 0)),  # Top Red
        OpposingRobot(Color.BLUE, Pose2D(30, 144, 0)),  # Bottom Blue
        OpposingRobot(Color.BLUE, Pose2D(-30, 144, 0)),  # Top Blue
    ]

    return FieldRepresentation(goals=goal_arr, robots=robot_arr)


def basic_ring_representation():
    ring_arr = [
        Ring(Pose2D(-69, 72, 0)),  # Top L
        Ring(Pose2D(-62, 72, 0)),
        Ring(Pose2D(-55, 72, 0)),
        Ring(Pose2D(-48, 72, 0)),
        Ring(Pose2D(-48, 78, 0)),
        Ring(Pose2D(-48, 84, 0)),
        Ring(Pose2D(-48, 90, 0)),
        Ring(Pose2D(-48, 96, 0)),
        Ring(Pose2D(-25, 72, 0)),  # Top-Mid Line
        Ring(Pose2D(-17, 72, 0)),
        Ring(Pose2D(-9, 72, 0)),
        Ring(Pose2D(9, 72, 0)),  # Bottom-Mid Line
        Ring(Pose2D(17, 72, 0)),
        Ring(Pose2D(25, 72, 0)),
        Ring(Pose2D(69, 72, 0)),  # Bottom L
        Ring(Pose2D(62, 72, 0)),
        Ring(Pose2D(55, 72, 0)),
        Ring(Pose2D(48, 72, 0)),
        Ring(Pose2D(48, 66, 0)),
        Ring(Pose2D(48, 60, 0)),
        Ring(Pose2D(48, 54, 0)),
        Ring(Pose2D(48, 48, 0)),
    ]

    robot_arr = [
        HostRobot(Color.RED, Pose2D(30, 0, 0)),  # Bottom Red
        PartnerRobot(Color.RED, Pose2D(-30, 0, 0)),  # Top Red
        OpposingRobot(Color.BLUE, Pose2D(30, 144, 0)),  # Bottom Blue
        OpposingRobot(Color.BLUE, Pose2D(-30, 144, 0)),  # Top Blue
    ]

    return FieldRepresentation(rings=ring_arr, robots=robot_arr)


def starting_representation():
    ring_arr = [
        Ring(Pose2D(-69, 72, 0)),  # Top L
        Ring(Pose2D(-62, 72, 0)),
        Ring(Pose2D(-55, 72, 0)),
        Ring(Pose2D(-48, 72, 0)),
        Ring(Pose2D(-48, 78, 0)),
        Ring(Pose2D(-48, 84, 0)),
        Ring(Pose2D(-48, 90, 0)),
        Ring(Pose2D(-48, 96, 0)),
        Ring(Pose2D(-25, 72, 0)),  # Top-Mid Line
        Ring(Pose2D(-17, 72, 0)),
        Ring(Pose2D(-9, 72, 0)),
        Ring(Pose2D(9, 72, 0)),  # Bottom-Mid Line
        Ring(Pose2D(17, 72, 0)),
        Ring(Pose2D(25, 72, 0)),
        Ring(Pose2D(69, 72, 0)),  # Bottom L
        Ring(Pose2D(62, 72, 0)),
        Ring(Pose2D(55, 72, 0)),
        Ring(Pose2D(48, 72, 0)),
        Ring(Pose2D(48, 66, 0)),
        Ring(Pose2D(48, 60, 0)),
        Ring(Pose2D(48, 54, 0)),
        Ring(Pose2D(48, 48, 0)),
        Ring(Pose2D(-28, 48, 0)),  # Left Top Star
        Ring(Pose2D(-25, 45, 0)),
        Ring(Pose2D(-25, 48, 0)),
        Ring(Pose2D(-25, 51, 0)),
        Ring(Pose2D(-22, 48, 0)),
        Ring(Pose2D(-3, 48, 0)),  # Left Bottom Star
        Ring(Pose2D(0, 45, 0)),
        Ring(Pose2D(0, 48, 0)),
        Ring(Pose2D(0, 51, 0)),
        Ring(Pose2D(3, 48, 0)),
        Ring(Pose2D(-3, 95, 0)),  # Right Top Star
        Ring(Pose2D(0, 92, 0)),
        Ring(Pose2D(0, 95, 0)),
        Ring(Pose2D(0, 98, 0)),
        Ring(Pose2D(3, 95, 0)),
        Ring(Pose2D(22, 95, 0)),  # Right Bottom Star
        Ring(Pose2D(25, 92, 0)),
        Ring(Pose2D(25, 95, 0)),
        Ring(Pose2D(25, 98, 0)),
        Ring(Pose2D(28, 95, 0)),
    ]

    goal_arr = [
        RedGoal(Pose2D(60, 35, 0)),  # Bottom Red
        RedGoal(Pose2D(-36, 12, 0)),  # Top Red
        BlueGoal(Pose2D(-60, 109, 0)),  # Top Blue
        BlueGoal(Pose2D(36, 132, 0)),  # Bottom Blue
        LowNeutralGoal(Pose2D(-35, 72, 0)),  # Top Neutral
        HighNeutralGoal(Pose2D(0, 72, 0)),  # Mid Neutral
        LowNeutralGoal(Pose2D(35, 72, 0)),  # Bottom Neutral
    ]

    red_plat = RedPlatform(PlatformState.LEFT)

    blue_plat = BluePlatform(PlatformState.RIGHT)

    robot_arr = [
        HostRobot(Color.RED, Pose2D(48, 12, 0)),  # Bottom Red
        PartnerRobot(Color.RED, Pose2D(-48, 12, 0)),  # Top Red
        OpposingRobot(Color.BLUE, Pose2D(48, 132, 0)),  # Bottom Blue
        OpposingRobot(Color.BLUE, Pose2D(-48, 132, 0)),  # Top Blue
    ]

    return FieldRepresentation(
        rings=ring_arr,
        goals=goal_arr,
        red_platform=red_plat,
        blue_platform=blue_plat,
        robots=robot_arr,
    )


def ending_representation():
    ring_arr = [
        Ring(Pose2D(-69, 25, 0)),
        Ring(Pose2D(-62, 121, 0)),
        Ring(Pose2D(-55, 32, 0)),
        Ring(Pose2D(-44, 96, 0)),
        Ring(Pose2D(-25, 22, 0)),
        Ring(Pose2D(-17, 7, 0)),
        Ring(Pose2D(9, 72, 0)),
        Ring(Pose2D(19, 61, 0)),
        Ring(Pose2D(6, 99, 0)),
        Ring(Pose2D(48, 84, 0)),
        Ring(Pose2D(-28, 48, 0)),
        Ring(Pose2D(-25, 4, 0)),
        Ring(Pose2D(-22, 48, 0)),
        Ring(Pose2D(-3, 22, 0)),
        Ring(Pose2D(26, 45, 0)),
        Ring(Pose2D(0, 14, 0)),
        Ring(Pose2D(0, 51, 0)),
        Ring(Pose2D(23, 100, 0)),
        Ring(Pose2D(-3, 95, 0)),
        Ring(Pose2D(32, 104, 0)),
        Ring(Pose2D(22, 95, 0)),
        Ring(Pose2D(8, 95, 0)),
    ]

    goal_arr = [
        RedGoal(
            Pose2D(25, -63, 0),
            ring_containers={
                GoalLevel.BASE: RingContainer(
                    rings=[Ring(Pose2D(25, -63, 0)), Ring(Pose2D(25, -63, 0))]
                ),
                GoalLevel.LOW: RingContainer(
                    rings=[
                        Ring(Pose2D(25, -63, 0)),
                        Ring(Pose2D(25, -63, 0)),
                        Ring(Pose2D(25, -63, 0)),
                    ]
                ),
            },
        ),
        RedGoal(
            Pose2D(-49, 18, 0),
            ring_containers={
                GoalLevel.BASE: RingContainer(rings=[Ring(Pose2D(-49, 18, 0))])
            },
        ),
        LowNeutralGoal(
            Pose2D(-21, 38, 0),
            ring_containers={
                GoalLevel.BASE: RingContainer(
                    rings=[Ring(Pose2D(-21, 38, 0)), Ring(Pose2D(-21, 38, 0))]
                ),
                GoalLevel.LOW: RingContainer(
                    rings=[
                        Ring(Pose2D(-21, 38, 0)),
                        Ring(Pose2D(-21, 38, 0)),
                        Ring(Pose2D(-21, 38, 0)),
                        Ring(Pose2D(-21, 38, 0)),
                    ]
                ),
            },
        ),
        LowNeutralGoal(Pose2D(0, 72, 0), tipped=True),
    ]

    red_plat = RedPlatform(
        PlatformState.LEVEL,
        robots=[
            HostRobot(
                Color.RED,
                Pose2D(0, 4, 0),
                rings=[Ring(Pose2D(0, 4, 0)), Ring(Pose2D(0, 4, 0)), Ring(Pose2D(0, 4, 0))],
                goals=[
                    HighNeutralGoal(
                        Pose2D(0, 4, 0),
                        ring_containers={
                            GoalLevel.HIGH: RingContainer(
                                rings=[
                                    Ring(Pose2D(0, 4, 0)),
                                    Ring(Pose2D(0, 4, 0)),
                                    Ring(Pose2D(0, 4, 0)),
                                    Ring(Pose2D(0, 4, 0)),
                                    Ring(Pose2D(0, 4, 0)),
                                ]
                            )
                        },
                    )
                ],
            )
        ],
    )

    blue_plat = BluePlatform(
        PlatformState.LEVEL,
        goals=[
            BlueGoal(
                Pose2D(0, 141, 0),
                ring_containers={
                    GoalLevel.LOW: RingContainer(
                        rings=[
                            Ring(Pose2D(0, 141, 0)),
                            Ring(Pose2D(0, 141, 0)),
                            Ring(Pose2D(0, 141, 0)),
                            Ring(Pose2D(0, 141, 0)),
                            Ring(Pose2D(0, 141, 0)),
                        ]
                    )
                },
            ),
        ],
        robots=[
            OpposingRobot(Color.BLUE, Pose2D(-10, 142, 0)),
            OpposingRobot(
                Color.BLUE, Pose2D(14, 141, 0), goals=[BlueGoal(Pose2D(14, 141, 0))]
            ),
        ],
    )

    robot_arr = [PartnerRobot(Color.RED, Pose2D(-49, 71, 0), tipped=True)]

    return FieldRepresentation(
        rings=ring_arr,
        goals=goal_arr,
        red_platform=red_plat,
        blue_platform=blue_plat,
        robots=robot_arr,
    )
