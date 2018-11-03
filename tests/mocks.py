from typing import Any, Dict, Callable
import unittest.mock
from flask_jwt import rules


patch_object = unittest.mock.patch.object


def raise_error(ex) -> Callable:
    def _raise(*_: Any, **__: Any) -> None:
        raise ex

    return _raise


class MockRule(rules.JWTRule):
    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self, _):
        return self.return_value


class MockStore:
    def __init__(self, obj=None):
        self.obj = obj or {}

    def get(self) -> Dict:
        return self.obj

    def set(self, obj: Dict) -> None:
        self.obj = obj


class MockRequest:
    def __init__(
        self,
        headers: Dict = None,
        json: Dict = None,
        args: Dict = None,
        form: Dict = None,
        view_args: Dict = None,
    ):
        self.headers = headers or {}
        self.json = json
        self.args = args
        self.form = form
        self.view_args = view_args


class FakeG:
    ...
