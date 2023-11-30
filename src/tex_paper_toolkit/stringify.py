"""
Module that contains utilities for generating valid TeX strings, identifiers
and labels.
"""

import re

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


def make_tex_identifier(
    identifier: str, spell_digits=False, upcase_after_separator=False
) -> str:
    """
    Creates a valid TeX identifier from the given base string.
    The string is first tokenized by removing invalid TeX characters.

    Parameters
    ----------
    identifier : str
        The string that should be converted.
    spell_digits : bool (default: False)
        Specifies whether numbers contained within the string could be spelled
        instead. Otherwise, numbers are omitted.
    upcase_after_separator : bool (default: False)
        Capitalizes individual parts of the string that appear after separation.

    Returns
    -------
    str
        A valid TeX string created from the given identifier.
    """
    identifier_parts = identifier.split(r"[/\s:.,_-]")

    if upcase_after_separator:
        identifier_parts = [part.capitalize() for part in identifier_parts]

    tex_identifier = "".join(identifier_parts)

    if spell_digits:

        def is_num(c: str) -> bool:
            return c >= "0" and c <= "9"

        tex_identifier = "".join(
            [(DIGIT_LABELS[int(c)] if is_num(c) else c) for c in tex_identifier]
        )
    else:
        tex_identifier = re.sub(r"\d", "", tex_identifier)
    return tex_identifier
