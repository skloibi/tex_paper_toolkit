"""
Module for base mixins that add functionality to the toolkit.
The default mixins offer support for defining Tex constants or simply
serializing strings.
"""

from typing import Any, Self, Optional, Protocol
from pathlib import Path
from abc import abstractmethod
from tex_paper_toolkit.stringify import make_tex_identifier
from tex_paper_toolkit.serialization import Serializable, SerTarget


# pylint: # pylint: disable=too-few-public-methods
class ToolkitMixin(Protocol):
    """
    Abstract protocol for `TexToolkit` mixins.
    """

    @abstractmethod
    def add(self, s: Serializable):
        ...


class NewCommand(Serializable):
    """
    Defines a serializable TeX constant definition (\\newcommand{<label>}{<value>}).
    """

    # pylint: # pylint: disable=too-many-arguments
    def __init__(
        self,
        label: str,
        value: Any,
        comment: Optional[Any] = None,
        mathmode: bool = True,
        unit: str = "",
        str_format: str = "d",
        spell_digits: bool = False,
        upcase_after_separator=False,
        to_file: Optional[SerTarget] = None,
    ) -> None:
        super().__init__(label, to_file)
        self.__value = value
        self.__comment = comment
        self.__mathmode = mathmode
        self.__unit = unit
        self.__str_format = str_format
        self.__spell_digits = spell_digits
        self.__upcase_after_separator = upcase_after_separator

    def serialize(self) -> str:
        value_str = f"{self.__value:{self.__str_format}}{self.__unit}"
        if self.__mathmode:
            value_str = f"${value_str}$"

        suffix = f" % {self.__comment}" if self.__comment else ""

        label = make_tex_identifier(
            self.key, self.__spell_digits, self.__upcase_after_separator
        )

        return f"\\newcommand{{\\{label}}}{{{value_str}}}{suffix}"


class NewCommandMixin(ToolkitMixin):
    """
    A toolkit mixin that enables definition of `NewCommand`s.
    """

    def newcommand(
        self,
        label: str,
        value: Any,
        comment: Any = None,
        mathmode: bool = True,
        unit: str = "",
        str_format: str = "d",
        spell_digits: bool = False,
        upcase_after_separator=False,
        to_file: Optional[SerTarget] = None,
        command: NewCommand | None = None,
    ) -> Self:
        """
        DSL method to register a `NewCommand`, either by passing an instance directly
        or by providing the necessary arguments.
        """

        if not command:
            command = NewCommand(
                label,
                value,
                comment,
                mathmode,
                unit,
                str_format,
                spell_digits,
                upcase_after_separator,
                to_file,
            )
        return self.add(command)


class TexString(Serializable):
    """
    A serializable TeX string definition.
    """

    def __init__(
        self, key: Any, tex_str: str, to_file: Optional[str | Path] = None
    ) -> None:
        super().__init__(key, to_file)
        self.__tex_str = tex_str

    def serialize(self) -> str:
        return self.__tex_str


class AnyStringMixin(ToolkitMixin):
    """
    A toolkit mixin that enables generation of arbitrary TeX text.
    """

    def texstring(
        self,
        label: str,
        tex_str: str | TexString,
        to_file: Optional[str | Path] = None,
    ) -> Self:
        elem = (
            tex_str
            if isinstance(tex_str, TexString)
            else TexString(label, tex_str, to_file)
        )
        return self.add(elem)
