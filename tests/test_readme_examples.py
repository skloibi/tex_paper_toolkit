# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from pyfakefs.fake_filesystem import FakeFilesystem
from utils import assert_file_content


# pylint: disable=unused-argument
def test_generates_minimal_samples(fs: FakeFilesystem):
    import readme.minimal_example  # pylint: disable=import-error,unused-import,import-outside-toplevel

    assert_file_content(
        "tex_output.tex",
        r"""\newcommand{\constantOne}{$1$}
\newcommand{\constanttwo}{$2$}
\emph{Emphasized text}
""",
    )
    assert_file_content(
        "tex_texstring_output.tex", "\\textbf{Text in a different file!}\n"
    )


# pylint: disable=unused-argument
def test_generates_custom_mixins_samples(fs: FakeFilesystem):
    import readme.custom_mixins_example  # pylint: disable=import-error,unused-import,import-outside-toplevel

    assert_file_content(
        "tex_output.tex",
        r"""\newcommand{\const}{3}
\textbf{This is just some random tex code that should also appear in the file}
\texttt{val x = 10}
""",
    )
