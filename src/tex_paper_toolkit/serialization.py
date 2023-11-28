from typing import Generic, TypeVar, Optional, Union
from pathlib import Path
from tex_paper_toolkit.stringify import make_tex_identifier
from abc import abstractmethod, ABCMeta

T = TypeVar("T")

SerTarget = Union[str, Path, "Serializer"]


class Serializable(Generic[T], metaclass=ABCMeta):
    """
    Abstract base class for types that define components that are serializable
    to TeX contents. The `serialize` method should yield a valid TeX string.
    """

    def __init__(self, key: T, target: Optional[SerTarget] = None) -> None:
        """ """
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
            Either a path object or a serializer object that describes
        """
        target = self.__target
        if isinstance(target, Path):
            return target
        elif isinstance(target, str):
            return Path(target)
        elif isinstance(target, Serializer):
            return target
        else:
            assert target is None, f"Unexpected target {target}"
            return default_path

    @abstractmethod
    def serialize(self) -> str:
        pass

    @property
    def key(self) -> T:
        return self.__key

    @property
    def id(self) -> str:
        return "%s:%s" % (type(self), self.key)


TS = TypeVar("TS", bound=Serializable)


class Serializer(Generic[TS], metaclass=ABCMeta):
    """
    A custom serializer that can be given to `Serializable`s.
    """

    @abstractmethod
    def serialize(self, serializable: TS):
        pass
