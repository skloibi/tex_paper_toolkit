# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods

from pathlib import Path
from typing import Callable, Optional

from tex_paper_toolkit import SerTarget, Serializable, Serializer


class CustomSerializable(Serializable[str]):
    def __init__(self, key: str, target: Optional[SerTarget], action: Callable) -> None:
        super().__init__(key, target)
        self.__action = action

    def serialize(self):
        self.__action(self)


class NopSerializable(Serializable[str]):
    def __init__(self, key: str, target: SerTarget | None = None) -> None:
        super().__init__(key, target)

    def serialize(self) -> str:
        return self.key


class CustomSerializer(Serializer[NopSerializable]):
    def __init__(self, action: Callable) -> None:
        super().__init__()
        self.__action = action

    def serialize(self, serializable: NopSerializable):
        return self.__action(serializable)


def test_get_path_or_default():
    default_path = Path("/tmp/default_file")
    t0 = "str_target"
    t1 = Path("/tmp/test_file")
    t2 = CustomSerializer(lambda s: s.key)
    assert (
        NopSerializable("key", None).get_path_or_default(default_path) == default_path
    )
    assert NopSerializable("key", t0).get_path_or_default(default_path) == Path(t0)
    assert NopSerializable("key", t1).get_path_or_default(default_path) == t1
    assert NopSerializable("key", t2).get_path_or_default(default_path) == t2
