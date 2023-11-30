"""
Module that handles serialization of toolkit elements and defines abstract base
types for custom extensions.
"""

from abc import abstractmethod, ABCMeta
from typing import Generic, TypeVar, Optional, Union
from pathlib import Path

T = TypeVar("T")

"""
By default, we can either specify a string or Path path or define a custom
serialization handler.
"""
SerTarget = Union[str, Path, "Serializer"]


class Serializable(Generic[T], metaclass=ABCMeta):
    """
    Abstract base class for types that define components that are serializable
    to TeX contents. The `serialize` method should yield a valid TeX string.
    """

    def __init__(self, key: T, target: Optional[SerTarget] = None) -> None:
        """
        Creates a new `Serializable` with the given key that should be unique
        within its category of implementations and an optional target
        description that defines the serialization method.

        Parameters
        ----------
        key : T
            A key that should uniquely identify an instance within its
            `Serializable` implementation category.
        target : String | Path | Serializer | None
            An optional serialization target that either specifies the target
            location or a custom serialization method.
        """
        self.__key = key
        self.__target = target

    def get_path_or_default(self, default_path: Path) -> "Path | Serializer":
        """
        Returns the target path associated with this object or the provided
        default if no path was specified.

        Parameters
        ----------
        default_path : Path
            The default path to use if no `self.__target` was specified.

        Returns
        -------
        Path | Serializer
            Either a path object or a serializer object that defines how the
            given `Serializable` is transformed upon serialization.
        """
        target = self.__target
        if isinstance(target, Path):
            return target
        if isinstance(target, str):
            return Path(target)
        if isinstance(target, Serializer):
            return target

        assert target is None, f"Unexpected target {target}"
        return default_path

    @abstractmethod
    def serialize(self) -> str:
        """
        Generate a valid TeX string from this `Serializable`.

        Returns
        -------
        str
            A valid TeX string representing this `Serializable`
        """
        ...

    @property
    def key(self) -> T:
        """
        Returns a unique key for this `Serializable` within its implementation category.
        I.e., for each implementation, this key should be unique per created instance.

        Returns
        -------
        T
            The unique key identifying this `Serializable` within its category of
            implementations.
        """
        return self.__key

    @property
    def id(self) -> str:
        """
        Generate a unique identifier for this `Serializable` to detect duplicates
        during serialization of all values (as duplicate definitions could cause TeX issues).

        Returns
        -------
        str
            A (ideally) unique string representing this `Serializable`
        """
        return f"{type(self)}:{self.key}"


TS = TypeVar("TS", bound=Serializable)


class Serializer(Generic[TS], metaclass=ABCMeta):
    """
    A base class for custom serializers that can be provided to `Serializable`s.
    This is an alternative to default serialization which simply writes the
    strings to a file.
    """

    @abstractmethod
    def serialize(self, serializable: TS) -> None:
        """
        Serializes the given `Serializable`.

        Parameters
        ----------
        serializable : TS
            The target that should be serialized
        """
        ...
