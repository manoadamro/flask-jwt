import unittest
import flask_jwt


class AnyOfTest(unittest.TestCase):
    def test_any_of(self):
        rule = flask_jwt.rules.AnyOf(lambda _: True, lambda _: False)
        self.assertTrue(rule({}))

    def test_fails(self):
        rule = flask_jwt.rules.AnyOf(lambda _: False, lambda _: False)
        self.assertFalse(rule({}))
