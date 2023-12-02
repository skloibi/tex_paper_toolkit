# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from abc import ABCMeta
from pathlib import Path
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from utils import assert_file_content
from tex_paper_toolkit.serialization import Serializable, Serializer
from tex_paper_toolkit.toolkit import TexToolkit


class AppenderToolkit(TexToolkit):
    pass


def append_to(l: list[str]) -> Serializer:
    return lambda s: l.append(s.serialize())


class SimpleSerializable(Serializable[str], metaclass=ABCMeta):
    def serialize(self) -> str:
        return self.id


class Appender(SimpleSerializable):
    def __init__(self, key: str, to_list: list[str]) -> None:
        super().__init__(key, append_to(to_list))


class Stringifier(SimpleSerializable):
    def __init__(self, key: str) -> None:
        super().__init__(key, None)


class FileWriter(SimpleSerializable):
    def __init__(self, key: str, path: str) -> None:
        super().__init__(key, Path(path))


# pylint: disable=unused-argument
def test_custom_toolkit_serialize(fs: FakeFilesystem):
    tex = AppenderToolkit()

    res = list[str]()

    tex.add(Appender("mystr", res))
    tex.add(Appender("mystr", res))
    tex.add(Appender("mystr2", res))

    tex.serialize(to_file="should_not_be_created.tex")

    assert not Path("should_not_be_created.tex").exists()
    assert res == ["Appender:mystr", "Appender:mystr2"]


# pylint: disable=unused-argument
def test_custom_toolkit_serialize_mixed_targets(fs: FakeFilesystem):
    tex = AppenderToolkit()

    res = list[str]()
    tex.add(Appender("a", res))
    tex.add(Appender("b", res))
    tex.add(Stringifier("c"))
    tex.add(FileWriter("d", "d.tex"))
    tex.add(FileWriter("e", "e.tex"))
    tex.add(Stringifier("f"))

    tex.serialize(to_file="default_outfile.tex")

    assert res == ["Appender:a", "Appender:b"]
    assert_file_content("default_outfile.tex", "Stringifier:c\nStringifier:f\n")
    assert_file_content("d.tex", "FileWriter:d\n")
    assert_file_content("e.tex", "FileWriter:e\n")


# pylint: disable=unused-argument
def test_serialize_invalid_path(fs: FakeFilesystem):
    tex = AppenderToolkit()

    res = list[str]()
    tex.add(Appender("xyz", res))

    mydir = Path("mydir")
    mydir.mkdir()

    with pytest.raises(FileExistsError):
        tex.serialize(to_file="mydir")

    assert len(res) == 0
