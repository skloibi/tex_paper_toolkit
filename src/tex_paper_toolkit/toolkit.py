"""
Module that defines the default toolkit type and provides a base implementation
with the default mixins.
"""

from collections import defaultdict
from typing import Self
from pathlib import Path
from abc import ABCMeta
from tex_paper_toolkit.serialization import Serializable, Serializer
from tex_paper_toolkit.mixins import AnyStringMixin, NewCommandMixin, ToolkitMixin


class TexToolkit(ToolkitMixin, metaclass=ABCMeta):
    """
    Abstract base class that represents the toolkit that captures TeX
    serializable components and enables extension with DSL methods via
    mixins.
    """

    def __init__(self) -> None:
        self._targets: dict[str, Serializable] = {}

    def add(self, s: Serializable) -> Self:
        self._targets[s.id] = s
        return self

    def serialize(self, to_file: str | Path) -> None:
        """
        Serializes all registered `Serializable`s to the given output file or
        by using individually specified `Serializer`s.

        Parameters
        ----------
        to_file : str | Path
            The file path to which the serialized components are written by
            default.
        """
        path: Path = Path(to_file) if isinstance(to_file, str) else to_file
        if path.exists() and not path.is_file():
            raise FileExistsError(
                "Element at path", path, "exists and is not a writable file"
            )

        target_locations = defaultdict[Path, list[Serializable]](list)

        for target in self._targets.values():
            ser_target = target.get_path_or_default(path)
            if isinstance(ser_target, Serializer):
                ser_target.serialize(target)
            else:
                target_locations[ser_target].append(target)

        for path, entries in target_locations.items():
            with open(path, "w", encoding="UTF-8") as outfile:
                for entry in entries:
                    outfile.write(entry.serialize() + "\n")


class DefaultToolkit(NewCommandMixin, AnyStringMixin, TexToolkit):
    """
    A default implementation of the `TexToolkit` that enables generation of
    `\\newcommand` constants as well as arbitrary Tex strings.
    """
