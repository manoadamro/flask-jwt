from typing import Any, Dict, Callable
import unittest.mock


patch_object = unittest.mock.patch.object


def raise_error(ex) -> Callable:
    def _raise(*_: Any, **__: Any) -> None:
        raise ex

    return _raise


class MockStore:
    def __init__(self, obj=None):
        self.obj = obj or {}

    def get(self) -> Dict:
        return self.obj

    def set(self, obj: Dict) -> None:
        self.obj = obj


class MockRequest:
    def __init__(self, headers: Dict = None):
        self.headers = headers or {}


class FakeG:
    ...
