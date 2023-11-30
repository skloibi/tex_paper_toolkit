#!/usr/bin/env python
"""
tex_paper_toolkit is a library that simplifies export of values and texts into TeX format
and can be used when analyzing/evaluating data for a paper.
"""
from tex_paper_toolkit.mixins import (
    ToolkitMixin,
    AnyStringMixin,
    TexString,
    NewCommand,
    NewCommandMixin,
)
from tex_paper_toolkit.serialization import Serializable, Serializer, SerTarget
from tex_paper_toolkit.stringify import make_tex_identifier
from tex_paper_toolkit.toolkit import TexToolkit, DefaultToolkit
from tex_paper_toolkit.version import __version__

__all__ = [
    "__version__",
    "ToolkitMixin",
    "AnyStringMixin",
    "TexString",
    "NewCommand",
    "NewCommandMixin",
    "Serializable",
    "Serializer",
    "SerTarget",
    "make_tex_identifier",
    "TexToolkit",
    "DefaultToolkit",
]
