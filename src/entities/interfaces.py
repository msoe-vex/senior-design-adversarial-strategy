import json
from abc import ABC, abstractmethod
from entities.enumerations import Color


class ITippable(ABC):
    @abstractmethod
    def is_tipped(self) -> bool:
        pass


class IScorable(ABC):
    @abstractmethod
    def get_current_score(self, color: Color) -> int:
        pass


class ISerializable:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
