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
    classname: str = field(init=False)

    def __post_init__(self):
        self.classname = type(self).__name__

    def __parse_ring_container(self, ring_container_dict: dict) -> RingContainer:
        pass

    def parse_representation(self, representation: str):
        for ring in representation["rings"]:
            x = ring["position"]["x"]
            y = ring["position"]["y"]
            pose = Pose2D(x, y)
            self.rings.append(Ring(pose))

        for goal in representation["goals"]:
            color = goal["color"]

            ring_containers = {}

            base_ring_container = goal["ring_containers"].get("BASE")

            if base_ring_container:
                ring_containers[GoalLevel.BASE] = self.__parse_ring_container()

            low_ring_container = goal["ring_containers"].get("LOW")

            if low_ring_container:
                pass

            high_ring_container = goal["ring_containers"].get("HIGH")

            if high_ring_container:
                pass

            x = goal["position"]["x"]
            y = goal["position"]["y"]
            pose = Pose2D(x, y)

            tipped = goal["tipped"]

    def as_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FieldState(ISerializable):
    def __init__(self, representation: Field, time: int):
        self.potential_score = (0, 0)
        self.current_time = time
        self.field_representation = representation
        self.classname = type(self).__name__

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
