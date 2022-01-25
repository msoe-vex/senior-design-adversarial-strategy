from __future__ import annotations
import json
from typing import List, Tuple
from dataclasses import dataclass, field
from entities.enumerations import Color
from entities.interfaces import ISerializable
from entities.math_utils import Pose2D
from entities.platforms import Platform, PlatformState, RedPlatform, BluePlatform
from entities.scoring_elements import BlueGoal, GoalLevel, Goal, NeutralGoal, RedGoal, Ring, RingContainer
from entities.robots import HostRobot, OpposingRobot, PartnerRobot, Robot, RobotID


@dataclass
class Field(ISerializable):
    rings: List[Ring] = field(default_factory=list)
    goals: List[Goal] = field(default_factory=list)
    red_platform: RedPlatform = RedPlatform(PlatformState.LEVEL)
    blue_platform: BluePlatform = BluePlatform(PlatformState.LEVEL)
    robots: List[Robot] = field(default_factory=list)

    def __parse_position(self, position_dict: dict) -> Pose2D:
        x = position_dict["x"]
        y = position_dict["y"]
        return Pose2D(x, y)

    def __parse_rings(self, ring_dict: dict) -> List[Ring]:
        rings = []
        for ring in ring_dict:
            pose = self.__parse_position(ring["position"])
            rings.append(Ring(pose))

        return rings

    def __parse_ring_container(self, ring_container_dict: dict) -> RingContainer:
        max_storage = ring_container_dict["max_storage"]

        rings = self.__parse_rings(ring_container_dict["rings"])

        return RingContainer(max_storage, rings)

    def __parse_ring_containers(self, ring_containers_dict: dict) -> dict[GoalLevel, RingContainer]:
        ring_containers = {}

        base_ring_container = ring_containers_dict.get("BASE")

        if base_ring_container:
            ring_containers[GoalLevel.BASE] = self.__parse_ring_container(base_ring_container)

        low_ring_container =ring_containers_dict.get("LOW")

        if low_ring_container:
            ring_containers[GoalLevel.LOW] = self.__parse_ring_container(low_ring_container)

        high_ring_container = ring_containers_dict.get("HIGH")

        if high_ring_container:
            ring_containers[GoalLevel.HIGH] = self.__parse_ring_container(high_ring_container)

        return ring_containers

    def __parse_goals(self, goal_dict: dict) -> List[Goal]:
        goals = []
        for goal in goal_dict:
            color = goal["color"]         

            pose = self.__parse_position(goal["position"])

            ring_containers = self.__parse_ring_containers(goal["ring_containers"])

            tipped = goal["tipped"]

            if color == Color.RED:
                goals.append(RedGoal(pose, ring_containers=ring_containers, tipped=tipped))
            elif color == Color.BLUE:
                goals.append(BlueGoal(pose, ring_containers=ring_containers, tipped=tipped))
            else:
                goals.append(NeutralGoal(pose, ring_containers=ring_containers, tipped=tipped))

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
                robots.append(HostRobot(color, pose, rings=rings, goals=goals, tipped=tipped))
            elif id == RobotID.PARTNER:
                robots.append(PartnerRobot(color, pose, rings=rings, goals=goals, tipped=tipped))
            else:
                robots.append(OpposingRobot(color, pose, rings=rings, goals=goals, tipped=tipped))

        return robots

    def __parse_platform(self, platform_dict: dict) -> Platform:
        color = platform_dict["color"]

        goals = self.__parse_goals(platform_dict["goals"])

        rings = self.__parse_rings(platform_dict["rings"])

        robots = self.__parse_robots(platform_dict["robots"])

        state = platform_dict["state"]

        if color == Color.RED:
            return RedPlatform(state, rings=rings, goals=goals, robots=robots)
        else:
            return BluePlatform(state, rings=rings, goals=goals, robots=robots)

    def parse_representation(self, representation: str) -> None:
        self.rings = self.__parse_rings(representation["rings"])

        self.goals = self.__parse_goals(representation["goals"])

        self.red_platform = self.__parse_platform(representation["red_platform"])
        
        self.blue_platform = self.__parse_platform(representation["blue_platform"])

        self.robots = self.__parse_robots(representation["robots"])

    def as_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FieldState(ISerializable):
    def __init__(self, representation: Field, time: int):
        self.potential_score = (0, 0)
        self.current_time = time
        self.field_representation = representation

    def __calculate_potential_score(self) -> None:
        return None  # TODO

    def get_current_representation(self) -> Field:
        return self.field_representation

    def get_current_time(self) -> int:
        return self.current_time

    def get_potential_score(self) -> Tuple[int, int]:
        return self.potential_score

    def get_current_score(self) -> Tuple[int, int]:
        return self.potential_score if self.current_time <= 0 else (0, 0)
