from pathlib import Path
from pyfakefs.fake_filesystem import FakeFilesystem


def assert_file_content(path: Path, expected_content: str):
    with open(path, "r", encoding="UTF-8") as f:
        actual_content = f.read()
        assert actual_content == expected_content


def test_generates_minimal_samples(fs: FakeFilesystem):
    import minimal_example  # pylint: disable=unused-import

    outfile = Path("tex_output.tex")
    custom_outfile = Path("tex_texstring_output.tex")
    assert outfile.is_file()
    assert_file_content(
        outfile,
        r"""\newcommand{\constantOne}{$1$}
\newcommand{\constanttwo}{$2$}
\emph{Emphasized text}
""",
    )
    assert_file_content(custom_outfile, "\\textbf{Text in a different file!}\n")


def test_generates_custom_mixins_samples(fs: FakeFilesystem):
    import custom_mixins_example  # pylint: disable=unused-import

    default_outfile = Path("tex_output.tex")
    assert default_outfile.is_file(), f"No file {default_outfile} was generated"
    assert_file_content(
        default_outfile,
        r"""\newcommand{\const}{3}
\textbf{This is just some random tex code that should also appear in the file}
\texttt{val x = 10}
""",
    )
