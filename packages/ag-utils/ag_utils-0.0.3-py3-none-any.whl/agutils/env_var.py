from os import getenv
from typing import Any


class Empty:
    def __init__(self, *args, **kwarg):
        raise TypeError(f"Type `Empty` cannot be instantiated.")

class EnvVar:

    def __init__(self, name:str=Empty, default:Any=Empty, otype:type = Empty):
        value = getenv(name, Empty)
        if value is Empty:
            value = default
        if value is not Empty and otype is not Empty:
            if otype is bool:
                value = str(value).lower() == 'true' or str(value).lower() == '1'
            else:
                if not isinstance(value, otype):
                    value = otype(value)
        self.value = value

    def __set_name__(self, owner, name):
        if self.value is Empty:
            raise TypeError(f'Value {owner.__name__}.{name} cannot be `Empty`')
        self.arg_name = name

    def __get__(self, obj, owner):
        return self.value