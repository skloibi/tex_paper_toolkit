# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods

from pathlib import Path
from typing import Callable, Optional, TypeVar

from tex_paper_toolkit import SerTarget, Serializable, Serializer


class CustomSerializable(Serializable[str]):
    def __init__(
        self,
        key: str,
        target: Optional[SerTarget],
        action: Callable[["CustomSerializable"], str],
    ) -> None:
        super().__init__(key, target)
        self.__action = action

    def serialize(self) -> str:
        return self.__action(self)


class NopSerializable(Serializable[str]):
    def __init__(self, key: str, target: SerTarget | None = None) -> None:
        super().__init__(key, target)

    def serialize(self) -> str:
        return self.key


T = TypeVar("T", bound=Serializable)


def create_printer(action: Callable[[T], str]) -> Serializer[T]:
    return lambda serializable: print(action(serializable))


def test_get_path_or_default():
    default_path = Path("/tmp/default_file")
    t0 = "str_target"
    t1 = Path("/tmp/test_file")
    t2 = create_printer(lambda s: s.key)
    assert (
        NopSerializable("key", None).get_path_or_default(default_path) == default_path
    )
    assert NopSerializable("key", t0).get_path_or_default(default_path) == Path(t0)
    assert NopSerializable("key", t1).get_path_or_default(default_path) == t1
    assert NopSerializable("key", t2).get_path_or_default(default_path) == t2


def test_key():
    target = create_printer(lambda s: s.key)
    s1 = CustomSerializable("mykey", None, target)
    s2 = NopSerializable("mykey")
    s3 = CustomSerializable("anotherkey", None, target)
    s4 = NopSerializable("ID01233")
    assert s1.key == "mykey"
    assert s2.key == "mykey"
    assert s3.key == "anotherkey"
    assert s4.key == "ID01233"


def test_id():
    target = create_printer(lambda s: s.key)
    s1 = CustomSerializable("mykey", None, target)
    s2 = NopSerializable("mykey")
    s3 = CustomSerializable("anotherkey", None, target)
    assert s1.id == "CustomSerializable:mykey"
    assert s2.id == "NopSerializable:mykey"
    assert s3.id == "CustomSerializable:anotherkey"
