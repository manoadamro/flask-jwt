import unittest
import flask_jwt


class RuleTest(unittest.TestCase):
    def test_fails(self):
        rule = flask_jwt.rules.JWTRule()
        self.assertRaises(NotImplementedError, rule, "token")
