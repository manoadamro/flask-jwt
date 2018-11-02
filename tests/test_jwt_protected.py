import unittest
from . import mocks
import flask_jwt


class JWTProtectedTest(unittest.TestCase):
    def test_protected(self):
        rules = [mocks.MockRule(True), mocks.MockRule(True)]
        with mocks.patch_object(
            flask_jwt.handlers.JWTHandler, "current_token", lambda: "token"
        ):
            protected = flask_jwt.decorators.JWTProtected(*rules)
            self.assertTrue(protected(lambda: True)())

    def test_no_token(self):
        rules = [mocks.MockRule(True), mocks.MockRule(True)]
        with mocks.patch_object(
            flask_jwt.handlers.JWTHandler, "current_token", lambda: None
        ):
            protected = flask_jwt.decorators.JWTProtected(*rules)
            self.assertRaises(
                flask_jwt.errors.JWTValidationError, protected(lambda: True)
            )

    def test_fails_rule(self):
        rules = [mocks.MockRule(True), mocks.MockRule(False)]
        with mocks.patch_object(
            flask_jwt.handlers.JWTHandler, "current_token", lambda: "token"
        ):
            protected = flask_jwt.decorators.JWTProtected(*rules)
            self.assertRaises(
                flask_jwt.errors.JWTValidationError, protected(lambda: True)
            )
