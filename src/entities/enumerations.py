from enum import Enum
from typing import Tuple


class Color(int, Enum):
    RED = 0
    BLUE = 1
    NEUTRAL = 2


class GoalLevel(int, Enum):
    BASE = 1
    LOW = 3
    HIGH = 10


def convertColorToRGBA(color: Color) -> Tuple[float, float, float, float]:
    """
    Maps between the color enum and an RGBA value
    """
    if color == Color.RED:
        return (1, 0, 0, 1)
    elif color == Color.BLUE:
        return (0, 0, 1, 1)
    else:
        return (1, 1, 0, 1)
