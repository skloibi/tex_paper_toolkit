"""
Module containing test utilities.s
"""


from pathlib import Path


def assert_file_content(path: Path | str, expected_content: str) -> None:
    """
    Asserts that the file at the given path contains the given expected
    contents.

    Parameters
    ----------
    path : str | Path
        The path to the target file
    expected_content : str
        The expected string contents
    """
    if isinstance(path, str):
        path = Path(path)
    assert path.is_file(), f"Path {path} does not describe a valid file"
    with open(path, "r", encoding="UTF-8") as f:
        actual_content = f.read()
        assert actual_content == expected_content
