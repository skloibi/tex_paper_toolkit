"""
A simple example showcasing the use of custom mixins.
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-ancestors

from tex_paper_toolkit import DefaultToolkit, ToolkitMixin, Serializable


class TextttString(Serializable):
    """
    A custom mixin serializable that defines text that holds text that should be
    formatted with a monospace font.
    """

    def __init__(self, key, texttt_str):
        super().__init__(key)
        self.__texttt_str = texttt_str

    def serialize(self):
        return f"\\texttt{{{self.__texttt_str}}}"


class TextttMixin(ToolkitMixin):
    """
    A custom mixin that simply wraps the passed text in `\texttt{...}`.
    """

    def texttt(self, label, texttt_str):
        return self.add(TextttString(label, texttt_str))


# define a new toolkit by inheriting DefaultToolkit
# DefaultToolkit already includes some mixins, but we can also inject custom ones
class MyCustomToolkit(TextttMixin, DefaultToolkit):
    pass


# instantiate a toolkit object
tex = MyCustomToolkit()

# manually add new TeX (constant) definitions (\\newcommand)
tex.newcommand("const", 1)

# this overwrites the previous definition of 'constOne'
tex.newcommand("const", 3, mathmode=False)

# add custom TeX strings that should be directly serialized
tex.texstring(
    "msg1",
    r"\textbf{This is just some random tex code that should also appear in the file}",
)

# call our custom mixin method
tex.texttt("code1", "val x = 10")

print("SERIALIZING STUFF!!")

# serialize the saved contents to the given TeX file
tex.serialize(to_file="tex_output.tex")
