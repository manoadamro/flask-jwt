import unittest
import unittest.mock
import flask
from flask_jwt import rules, protection, handler


class FakeRule(rules.JWTProtectionRule):
    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self, _):
        if not self.return_value:
            raise rules.JWTRuleError
        return self.return_value


class AllOfTest(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)

    def test_one_pass(self):
        @protection.JWTProtected(
            rules.AnyOf(FakeRule(True), FakeRule(False), FakeRule(False))
        )
        def mock_method():
            return True

        with self.app.app_context():
            with unittest.mock.patch.object(
                flask, "g", {handler._G_KEY: {"thing": "123"}}
            ):
                self.assertTrue(mock_method())

    def test_multiple_pass(self):
        @protection.JWTProtected(
            rules.AnyOf(FakeRule(True), FakeRule(True), FakeRule(True))
        )
        def mock_method():
            return True

        with self.app.app_context():
            with unittest.mock.patch.object(
                flask, "g", {handler._G_KEY: {"thing": "123"}}
            ):
                self.assertTrue(mock_method())

    def test_all_fail(self):
        @protection.JWTProtected(
            rules.AnyOf(FakeRule(False), FakeRule(False), FakeRule(False))
        )
        def mock_method():
            return True

        with self.app.app_context():
            with unittest.mock.patch.object(
                flask, "g", {handler._G_KEY: {"thing": "123"}}
            ):
                self.assertRaises(rules.JWTRuleError, mock_method)
