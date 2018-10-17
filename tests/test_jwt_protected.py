import unittest
import flask
from flask_jwt import protection, handler, rules


class FakeRule(rules.JWTProtectionRule):
    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self, *args, **kwargs):
        return self.return_value


@protection.JWTProtected(FakeRule(True), FakeRule(True))
def fake_method1(arg, kwarg=None):
    return f"arg={arg} kwarg={kwarg}"


@protection.JWTProtected(FakeRule(True), FakeRule(False))
def fake_method2(arg, kwarg=None):
    return f"arg={arg} kwarg={kwarg}"


class JWTProtectedTest(unittest.TestCase):
    def test_validates_token(self):
        token = {"scopes": ["thing1", "thing2", "thing3"]}
        flask.g[handler._G_KEY] = token
        self.assertEqual(
            fake_method1("thing", kwarg="thingy"), "arg=thing kwarg=thingy"
        )

    def test_raises_error_when_token_invalid(self):
        token = {"scopes": ["thing1", "thing2", "thing3"]}
        flask.g[handler._G_KEY] = token
        self.assertRaises(rules.JWTRuleError, fake_method2, "thing", kwarg="thingy")

    def test_raises_error_when_no_token(self):
        flask.g[handler._G_KEY] = None
        self.assertRaises(rules.JWTRuleError, fake_method1, "thing", kwarg="thingy")
