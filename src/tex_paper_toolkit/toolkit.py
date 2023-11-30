"""
Module that defines the default toolkit type and provides a base implementation
with the default mixins.
"""

from collections import defaultdict
from typing import Self
from pathlib import Path
from abc import ABCMeta
from tex_paper_toolkit.serialization import Serializable, Serializer
from tex_paper_toolkit.mixins import AnyStringMixin, NewCommandMixin


class TexToolkit(metaclass=ABCMeta):
    """
    Abstract base class that represents the toolkit that captures TeX
    serializable components and enables extension with DSL methods via
    mixins.
    """

    def __init__(self) -> None:
        self._targets: dict[str, Serializable] = {}

    def add(self, s: Serializable) -> Self:
        """
        Registers the given `Serializable` as part of this toolkit.
        If another `Serializable` from the same implementation with the same
        `id` is already registered, it is overwritten.

        Parameters
        ----------
        s : Serializable
            The `Serializable` that should be registered.

        Returns
        -------
        Self
            This toolkit object.
        """
        self._targets[s.id] = s
        return self

    def serialize(self, to_file: str | Path) -> None:
        import os

        path = Path(to_file) if isinstance(to_file, str) else to_file

        target_locations = defaultdict[Path, list[Serializable]](list)

        for target in self._targets.values():
            ser_target = target.get_path_or_default(path)
            if isinstance(ser_target, Serializer):
                ser_target.serialize(target)
            else:
                target_locations[ser_target].append(target)

        for path, entries in target_locations.items():
            with open(path, "w") as outfile:
                for entry in entries:
                    outfile.write(entry.serialize() + os.linesep)


class DefaultToolkit(NewCommandMixin, AnyStringMixin, TexToolkit):
    """
    A default implementation of the `TexToolkit` that enables generation of
    `\\newcommand` constants as well as arbitrary Tex strings.
    """
