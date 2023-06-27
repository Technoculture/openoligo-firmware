"""
Provides a Metaclass for creating Singleton classes.
"""
from typing import Any, Dict


class Singleton(type):
    """
    Metaclass for singleton classes.
    """

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
