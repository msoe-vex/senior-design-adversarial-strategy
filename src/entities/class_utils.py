from dataclasses import dataclass
from abc import ABC


@dataclass
class AbstractDataClass(ABC):
    """
    Abstract dataclass utility. Leveraging resource found at:

    https://stackoverflow.com/questions/60590442/abstract-dataclass-without-abstract-methods-in-python-prohibit-instantiation
    """

    def __new__(cls, *args, **kwargs):
        if cls == AbstractDataClass or cls.__bases__[0] == AbstractDataClass:
            raise TypeError("Instantiation of Abstract Class is Not Allowed.")
        return super().__new__(cls)
