import json
from typing import List
from dataclasses import dataclass, field
from entities.interfaces import ISerializable
from entities.math_utils import Pose2D
from entities.platforms import PlatformState, RedPlatform, BluePlatform
from entities.scoring_elements import GoalLevel, Goal, Ring, RingContainer
from entities.robots import Robot


@dataclass
class Field(ISerializable):
    rings: List[Ring] = field(default_factory=list)
    goals: List[Goal] = field(default_factory=list)
    red_platform: RedPlatform = RedPlatform(PlatformState.LEVEL)
    blue_platform: BluePlatform = BluePlatform(PlatformState.LEVEL)
    robots: List[Robot] = field(default_factory=list)

    def __parse_rings(self, ring_dict: dict) -> None:
        for ring in ring_dict:
            x = ring["position"]["x"]
            y = ring["position"]["y"]
            pose = Pose2D(x, y)
            self.rings.append(Ring(pose))

    def __parse_ring_container(self, ring_container_dict: dict) -> RingContainer:
        level = ring_container_dict["level"]
        max_storage = ring_container_dict["max_storage"]

        rings = []
        for ring in ring_container_dict["rings"]:
            x = ring["position"]["x"]
            y = ring["position"]["y"]
            pose = Pose2D(x, y)
            rings.append(pose)

        return RingContainer(level, max_storage, rings)

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

    def __parse_goals(self, goal_dict: dict) -> None:
        for goal in goal_dict:
            color = goal["color"]         

            x = goal["position"]["x"]
            y = goal["position"]["y"]
            pose = Pose2D(x, y)

            ring_containers = self.__parse_ring_containers(goal["ring_containers"])

            tipped = goal["tipped"]

            self.goals.append(Goal(color, pose, ring_containers, tipped))

    def __parse_red_platform(self, red_platform_dict: dict) -> None:
        pass # TODO

    def __parse_blue_platform(self, blue_platform_dict: dict) -> None:
        pass # TODO

    def __parse_robots(self, robots_dict: dict) -> None:
        pass # TODO

    def parse_representation(self, representation: str):
        self.__parse_rings(representation["rings"])

        self.__parse_goals(representation["goals"])

        self.__parse_red_platform(representation["red_platform"])
        
        self.__parse_blue_platform(representation["blue_platform"])

        self.__parse_robots(representation["robots"])

    def as_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FieldState(ISerializable):
    def __init__(self, representation: Field, time: int):
        self.potential_score = (0, 0)
        self.current_time = time
        self.field_representation = representation

    def __calculate_potential_score(self):
        return None  # TODO

    def get_current_representation(self) -> Field:
        return self.field_representation

    def get_current_time(self) -> int:
        return self.current_time

    def get_potential_score(self):
        return self.potential_score

    def get_current_score(self):
        return self.potential_score if self.current_time <= 0 else (0, 0)
