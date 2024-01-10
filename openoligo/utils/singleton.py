"""Provides a Metaclass for creating Singleton classes."""
from typing import Any, Dict


class Singleton(type):
    """Metaclass for singleton classes."""

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        """Override Call Method.

        overrides call method of the type to ensure that calls
        go to the same underlying object for various instances of theis class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)  # noqa: UP008
        return cls._instances[cls]
