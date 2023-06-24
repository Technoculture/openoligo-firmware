"""
A dict with fixed set of keys.
"""
from typing import TypeVar, Set, Generic, Optional

V = TypeVar("V")  # generic type for values


class FixedKeysDict(Generic[V]):
    """
    A dictionary-like class that allows attribute-based and dictionary-like
    access with a fixed set of keys and mutable values.
    """

    def __init__(self, valid_keys: Set[str]):
        """
        Initialize an instance of the class.

        Args:
            valid_keys (Set[str]): The valid keys for this dictionary.
        """
        self._valid_keys = valid_keys
        self._dict: dict[str, V] = {}

    def __setattr__(self, name: str, value: V) -> None:
        """
        Set an attribute. If the attribute is a valid key, the value is set
        in the internal dictionary. Otherwise, set the attribute normally.

        Args:
            name (str): The attribute name.
            value (V): The attribute value.
        """
        if name in self._valid_keys:
            self._dict[name] = value
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name: str) -> Optional[V]:
        """
        Get an attribute. If the attribute is a valid key, the value is fetched
        from the internal dictionary. If not a valid key, an AttributeError is raised.

        Args:
            name (str): The attribute name.

        Returns:
            The attribute value.

        Raises:
            AttributeError: If `name` is not a valid key.
        """
        if name in self._valid_keys:
            return self._dict.get(name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setitem__(self, key: str, value: V) -> None:
        """
        Set a key-value pair in the internal dictionary.

        Args:
            key (str): The key.
            value (V): The value.

        Raises:
            KeyError: If `key` is not a valid key.
        """
        if key not in self._valid_keys:
            raise KeyError(f"Invalid key: {key}")
        self._dict[key] = value

    def __getitem__(self, key: str) -> Optional[V]:
        """
        Get a value from the internal dictionary by its key.

        Args:
            key (str): The key.

        Returns:
            The value associated with `key`.

        Raises:
            KeyError: If `key` is not a valid key.
        """
        if key not in self._valid_keys:
            raise KeyError(f"Invalid key: {key}")
        return self._dict.get(key)

    def __str__(self) -> str:
        """
        Return a string representation of the internal dictionary.

        Returns:
            A string representation of the internal dictionary.
        """
        return str(self._dict)

    def __repr__(self) -> str:
        """
        Return a string representation of this instance.

        Returns:
            A string representation of this instance.
        """
        return f"{type(self).__name__}({self._dict})"
