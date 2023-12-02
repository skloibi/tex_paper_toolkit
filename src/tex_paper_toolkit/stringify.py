"""
Module that contains utilities for generating valid TeX strings, identifiers
and labels.
"""

import re
from typing import Literal

DIGIT_LABELS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


DigitSettings = Literal["c"] | bool


def make_tex_identifier(
    identifier: str, spell_digits: DigitSettings = False, upcase_after_separator=False
) -> str:
    """
    Creates a valid TeX identifier from the given base string.
    The string is first tokenized by removing invalid TeX characters.

    Parameters
    ----------
    identifier : str
        The string that should be converted.
    spell_digits : "c" | bool (default: False)
        Specifies whether numbers contained within the string could be spelled
        instead. Otherwise, numbers are omitted. The 'c' option additionally
        capitalizes the digit names after replacement.
    upcase_after_separator : bool (default: False)
        Capitalizes individual parts of the string that appear after separation.

    Returns
    -------
    str
        A valid TeX string created from the given identifier.
    """
    identifier_parts = re.split(r"[^a-zA-Z0-9]", identifier)

    if upcase_after_separator:
        identifier_parts = [part.capitalize() for part in identifier_parts]

    tex_identifier = "".join(identifier_parts)

    if spell_digits is not False:

        def is_num(c: str) -> bool:
            return "0" <= c <= "9"

        def write_out(c: str) -> str:
            ordinal = int(c)
            converted = DIGIT_LABELS[ordinal]
            return converted.capitalize() if spell_digits == "c" else converted

        tex_identifier = "".join(
            [(write_out(c) if is_num(c) else c) for c in tex_identifier]
        )
    else:
        tex_identifier = re.sub(r"\d", "", tex_identifier)
    return tex_identifier
