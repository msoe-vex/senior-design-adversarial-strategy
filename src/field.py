from serialization import ISerializable
from game_objects import RedPlatform, BluePlatform, PlatformState


class Field(ISerializable):
    def __init__(self, representation, time):
        self.__current_score = (0, 0)
        self.__current_time = time
        self.__field_representation = representation
        self.__classname = type(self).__name__

    def __calculate_current_score(self):
        return None # TODO

    def get_current_representation(self):
        return self.__field_representation

    def get_current_time(self):
        return self.__current_time

    def get_current_score(self):
        return self.__current_score


class FieldRepresentation(ISerializable):
    def __init__(self, representation):
        self.__rings = []
        self.__goals = []
        self.__red_platform = RedPlatform(PlatformState.LEVEL)
        self.__blue_platform = BluePlatform(PlatformState.LEVEL)
        self.__robots = []
        self.__classname = type(self).__name__

    def __parse_representation(self):
        return None # TODO

    def as_json():
        return None # TODO