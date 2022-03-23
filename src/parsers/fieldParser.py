from logging import getLogger
from typing import List, Tuple
from ..entities.constants import PARSER_LOGGER_NAME
from ..entities.enumerations import Color, GoalLevel
from ..entities.fieldRepresentation import FieldCounts, FieldRepresentation
from ..entities.mathUtils import Pose2D
from ..entities.platforms import BluePlatform, Platform, RedPlatform
from ..entities.robots import HostRobot, OpposingRobot, PartnerRobot, Robot, RobotID
from ..entities.scoring_elements import (
    BlueGoal,
    Goal,
    HighNeutralGoal,
    LowNeutralGoal,
    RedGoal,
    Ring,
    RingContainer,
)


class FieldParser:
    def __init__(self):
        self.field_counts = FieldCounts()

    def __parse_position(self, position_dict: dict) -> Pose2D:
        x = position_dict["x"]
        y = position_dict["y"]
        return Pose2D(x, y)

    def __parse_rings(self, ring_dict: dict) -> List[Ring]:
        rings = []
        for ring in ring_dict:
            pose = self.__parse_position(ring["position"])
            rings.append(Ring(pose))
            self.field_counts.rings += 1

        getLogger(PARSER_LOGGER_NAME).info(f"Rings parsed (Total: {len(rings)})")

        return rings

    def __parse_ring_container(self, ring_container_dict: dict) -> RingContainer:
        max_storage = ring_container_dict["max_storage"]

        rings = self.__parse_rings(ring_container_dict["rings"])

        getLogger(PARSER_LOGGER_NAME).info(
            f"Ring container parsed (Total: {len(rings)}, Max: {max_storage}"
        )

        return RingContainer(max_storage, rings)

    def __parse_ring_containers(
        self, ring_containers_dict: dict
    ) -> dict[GoalLevel, RingContainer]:
        ring_containers = dict()

        base_ring_container = ring_containers_dict.get("BASE")

        if base_ring_container:
            ring_containers[GoalLevel.BASE] = self.__parse_ring_container(
                base_ring_container
            )
            getLogger(PARSER_LOGGER_NAME).info("Ring container at level BASE parsed")
        else:
            ring_containers[GoalLevel.BASE] = RingContainer()
            getLogger(PARSER_LOGGER_NAME).info(
                "Ring container at level BASE not found, populating empty"
            )

        low_ring_container = ring_containers_dict.get("LOW")

        if low_ring_container:
            ring_containers[GoalLevel.LOW] = self.__parse_ring_container(
                low_ring_container
            )
            getLogger(PARSER_LOGGER_NAME).info("Ring container at level LOW parsed")
        else:
            ring_containers[GoalLevel.LOW] = RingContainer()
            getLogger(PARSER_LOGGER_NAME).info(
                "Ring container at level LOW not found, populating empty"
            )

        high_ring_container = ring_containers_dict.get("HIGH")

        if high_ring_container:
            ring_containers[GoalLevel.HIGH] = self.__parse_ring_container(
                high_ring_container
            )
            getLogger(PARSER_LOGGER_NAME).info("Ring container at level HIGH parsed")
        else:
            ring_containers[GoalLevel.HIGH] = RingContainer()
            getLogger(PARSER_LOGGER_NAME).info(
                "Ring container at level HIGH not found, populating empty"
            )

        return ring_containers

    def __parse_goals(self, goal_dict: dict) -> List[Goal]:
        goals = []

        for goal in goal_dict:
            color = goal["color"]
            level = goal["level"]

            pose = self.__parse_position(goal["position"])

            ring_containers = self.__parse_ring_containers(goal["ring_containers"])

            tipped = goal["tipped"]

            if color == Color.RED:
                goals.append(
                    RedGoal(pose, ring_containers=ring_containers, tipped=tipped)
                )
                self.field_counts.red_goals += 1
                getLogger(PARSER_LOGGER_NAME).info(f"Red goal parsed")
            elif color == Color.BLUE:
                goals.append(
                    BlueGoal(pose, ring_containers=ring_containers, tipped=tipped)
                )
                self.field_counts.blue_goals += 1
                getLogger(PARSER_LOGGER_NAME).info(f"Blue goal parsed")
            elif color == Color.NEUTRAL and level == GoalLevel.LOW:
                goals.append(
                    LowNeutralGoal(pose, ring_containers=ring_containers, tipped=tipped)
                )
                self.field_counts.low_neutral_goals += 1
                getLogger(PARSER_LOGGER_NAME).info(f"Low neutral goal parsed")
            elif color == Color.NEUTRAL and level == GoalLevel.HIGH:
                goals.append(
                    HighNeutralGoal(
                        pose, ring_containers=ring_containers, tipped=tipped
                    )
                )
                self.field_counts.high_neutral_goals += 1
                getLogger(PARSER_LOGGER_NAME).info(f"High neutral goal parsed")

        getLogger(PARSER_LOGGER_NAME).info(f"Goals parsed (Total: {len(goals)})")
        return goals

    def __parse_robots(self, robots_dict: dict) -> Robot:
        robots = []
        for robot in robots_dict:
            color = robot["color"]

            id = robot["id"]

            pose = self.__parse_position(robot["position"])

            rings = self.__parse_ring_containers(robot["rings"])

            goals = self.__parse_goals(robot["goals"])

            tipped = robot["tipped"]

            if id == RobotID.SELF:
                robots.append(
                    HostRobot(color, pose, rings=rings, goals=goals, tipped=tipped)
                )
                self.field_counts.host_robots += 1
                getLogger(PARSER_LOGGER_NAME).info("Host robot parsed")
            elif id == RobotID.PARTNER:
                robots.append(
                    PartnerRobot(color, pose, rings=rings, goals=goals, tipped=tipped)
                )
                self.field_counts.partner_robots += 1
                getLogger(PARSER_LOGGER_NAME).info("Partner robot parsed")
            else:
                robots.append(
                    OpposingRobot(color, pose, rings=rings, goals=goals, tipped=tipped)
                )
                self.field_counts.opposing_robots += 1
                getLogger(PARSER_LOGGER_NAME).info("Opposing robot parsed")

        getLogger(PARSER_LOGGER_NAME).info(f"Robots parsed (Total: {len(robots)})")
        return robots

    def __parse_platform(self, platform_dict: dict) -> Platform:
        color = platform_dict["color"]

        goals = self.__parse_goals(platform_dict["goals"])

        rings = self.__parse_rings(platform_dict["rings"])

        robots = self.__parse_robots(platform_dict["robots"])

        state = platform_dict["state"]

        if color == Color.RED:
            getLogger(PARSER_LOGGER_NAME).info("Red platform parsed")
            return RedPlatform(state, rings=rings, goals=goals, robots=robots)
        else:
            getLogger(PARSER_LOGGER_NAME).info("Blue platform parsed")
            return BluePlatform(state, rings=rings, goals=goals, robots=robots)

    def parse_representation(
        self, representation: str
    ) -> Tuple[FieldRepresentation, FieldCounts]:
        self.field_counts = FieldCounts()

        rings = self.__parse_rings(representation["rings"])

        goals = self.__parse_goals(representation["goals"])

        red_platform = self.__parse_platform(representation["red_platform"])

        blue_platform = self.__parse_platform(representation["blue_platform"])

        robots = self.__parse_robots(representation["robots"])

        return FieldRepresentation(
            red_platform=red_platform,
            blue_platform=blue_platform,
            rings=rings,
            goals=goals,
            robots=robots,
            field_counts=self.field_counts,
        )
