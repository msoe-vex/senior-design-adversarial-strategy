from dataclasses import dataclass, is_dataclass
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


def nested_dataclass(*args, **kwargs):
    """
    This class is a custom decorator to allow for nested dataclasses. Explanation can be found at:

    https://stackoverflow.com/questions/51564841/creating-nested-dataclass-objects-in-python
    """

    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                    new_obj = field_type(**value)
                    kwargs[name] = new_obj
            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper
