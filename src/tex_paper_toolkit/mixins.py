"""
Module for base mixins that add functionality to the toolkit.
The default mixins offer support for defining Tex constants or simply
serializing strings.
"""

from typing import Any, Self, Optional, Protocol
from tex_paper_toolkit.stringify import DigitSettings, make_tex_identifier
from tex_paper_toolkit.serialization import Serializable, SerTarget


# pylint: # pylint: disable=too-few-public-methods
class ToolkitMixin(Protocol):
    """
    Abstract protocol for `TexToolkit` mixins.
    """

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
        spell_digits: DigitSettings = False,
        upcase_after_separator: bool = False,
        to_file: Optional[SerTarget] = None,
    ) -> None:
        """
        Creates a new serializable `NewCommand` component.

        Parameters
        ----------
        label : str
            The label that is used as a name to uniquely identify this generated
            constant.

        value : Any
            The value of the TeX constant. Is converted to string upon
            serialization. Additional arguments can be used to customize the
            format during this conversion.

        comment : Any | None (default: None)
            An optional comment that is appended to the generated TeX string
            (separated with a TeX comment character `%`).

        mathmode : bool (default: True)
            Wraps the generated `value` via TeX "mathmode" markers
            (`$<value>$`).

        unit : str (default: "")
            An optional unit specifier to append to the `value`.

        str_format : str (default: "d")
            The format specifier to use when embedding the `value` into the
            generated TeX string.

        spell_digits : "c" | bool (default: False)
            Replaces digits within the label with their written-out names.

        upcase_after_separator: bool (default: False)
            Capitalizes individual words of the label.

        to_file : str | Path | Serializer | None (default: None)
            Optional serialization target.
        """
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

    # pylint: disable=too-many-arguments
    def newcommand(
        self,
        label: str,
        value: Any,
        comment: Any = None,
        mathmode: bool = True,
        unit: str = "",
        str_format: str = "d",
        spell_digits: DigitSettings = False,
        upcase_after_separator=False,
        to_file: Optional[SerTarget] = None,
        command: NewCommand | None = None,
    ) -> Self:
        """
        DSL method to register a `NewCommand`, either by passing an instance directly
        or by providing the necessary arguments.
        For documentation on the function's arguments, see the `NewCommand`
        constructor.
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
        self, key: Any, tex_str: str, to_file: Optional[SerTarget] = None
    ) -> None:
        """
        Creates a new serializable `TexString`.

        Parameters
        ----------
        key : Any
            The unique key that should identify this particular `TexString`.
        tex_str : str
            The TeX string. This has to be a valid TeX string as it will be
            serialized "as-is".
        to_file : str | Path | Serializer | None (default: None)
            Optional serialization target.
        """
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
        to_file: Optional[SerTarget] = None,
    ) -> Self:
        """
        DSL method to register a `TexString`, either by passing an instance directly
        or by providing the necessary arguments.
        For documentation on the function's arguments, see the `NewCommand`
        constructor.
        """
        elem = (
            tex_str
            if isinstance(tex_str, TexString)
            else TexString(label, tex_str, to_file)
        )
        return self.add(elem)
