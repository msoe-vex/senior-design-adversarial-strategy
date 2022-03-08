from abc import ABC


class AbstractClass(ABC):
    """
    Abstract class utility. Leveraging resource found at:

    https://stackoverflow.com/questions/60590442/abstract-dataclass-without-abstract-methods-in-python-prohibit-instantiation
    """

    def __new__(cls, *args, **kwargs):
        if cls == AbstractClass or cls.__bases__[0] == AbstractClass:
            raise TypeError("Instantiation of Abstract Class is Not Allowed.")
        return super().__new__(cls)
