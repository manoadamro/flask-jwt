import unittest
import flask_jwt


class NoneOfTest(unittest.TestCase):
    def test_any_of(self):
        rule = flask_jwt.rules.NoneOf(lambda _: False, lambda _: False)
        self.assertTrue(rule({}))

    def test_fails(self):
        rule = flask_jwt.rules.NoneOf(lambda _: False, lambda _: True)
        self.assertFalse(rule({}))
