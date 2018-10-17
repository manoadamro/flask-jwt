import unittest
import flask
from flask_jwt import protection, handler


@protection.JWTProtected(protection.HasScopes("thing", "other"))
def fake_method1(arg, kwarg=None):
    return f"arg={arg} kwarg={kwarg}"


class JWTProtectedTest(unittest.TestCase):
    def test_validates_scopes(self):
        flask.g[handler._G_KEY] = {"scopes": ["thing", "other", "third"]}
        self.assertEqual(
            fake_method1("thing", kwarg="thingy"), "arg=thing kwarg=thingy"
        )

    def test_raises_error_when_missing_scopes(self):
        flask.g[handler._G_KEY] = {"scopes": ["thing", "third"]}
        self.assertRaises(
            protection.JWTRuleError, fake_method1, "thing", kwarg="thingy"
        )
