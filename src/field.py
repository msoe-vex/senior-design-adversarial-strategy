import json
from typing import Tuple

from serialization import ISerializable
from game_objects import Pose2D, RedPlatform, BluePlatform, PlatformState


class Field(ISerializable):
    def __init__(self, representation: str, time: int):
        self.__potential_score = (0, 0)
        self.__current_time = time
        self.__field_representation = representation
        self.__classname = type(self).__name__

    def __calculate_potential_score(self):
        return None # TODO

    def get_current_representation(self) -> str:
        return self.__field_representation

    def get_current_time(self) -> int:
        return self.__current_time

    def get_potential_score(self) -> Tuple(int, int):
        return self.__potential_score

    def get_current_score(self) -> Tuple(int, int):
        return self.__potential_score if self.__current_time <= 0 else (0, 0)


class FieldRepresentation(ISerializable):
    def __init__(self, representation: str):
        self.__rings = []
        self.__goals = []
        self.__red_platform = RedPlatform(PlatformState.LEVEL)
        self.__blue_platform = BluePlatform(PlatformState.LEVEL)
        self.__robots = []
        self.__classname = type(self).__name__

    def __parse_representation(self):
        self_x = self.__parse_representation['robots']['host']['x']
        self_y = self.__parse_representation['robots']['host']['y']
        self_pos = Pose2D(self_x, self_y)
        
        for robot in self.representation['robots']:


        for ring in self.representation['rings']:
            x = ring['position']['x']
            y = ring['position']['y']
            currentPos
            dist = 
            self.__rings.append(Ring())

    def as_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)