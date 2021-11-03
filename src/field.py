import json
from typing import Tuple

from serialization import ISerializable
from game_objects import RedPlatform, BluePlatform, PlatformState


class Field(ISerializable):
    def __init__(self, rings=[], goals=[], red_platform=RedPlatform(PlatformState.LEVEL), blue_platform=BluePlatform(PlatformState.LEVEL), robots=[], field_representation=None):
        self.rings = rings
        self.goals = goals
        self.red_platform = red_platform
        self.blue_platform = blue_platform
        self.robots = robots
        self.field_representation = field_representation
        self.classname = type(self).__name__

        if field_representation is not None:
            self.__parse_representation()

    def __parse_representation(self):
        pass # Read in JSON data from self.__field_representation

    def as_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FieldState(ISerializable):
    def __init__(self, representation: Field, time: int):
        self.potential_score = (0, 0)
        self.current_time = time
        self.field_representation = representation
        self.classname = type(self).__name__

    def __calculate_potential_score(self):
        return None # TODO

    def get_current_representation(self) -> Field:
        return self.field_representation

    def get_current_time(self) -> int:
        return self.current_time

    def get_potential_score(self):
        return self.potential_score

    def get_current_score(self):
        return self.potential_score if self.current_time <= 0 else (0, 0)