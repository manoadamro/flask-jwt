import unittest
import flask_jwt


class AllOfTest(unittest.TestCase):
    def test_all_of(self):
        rule = flask_jwt.rules.AllOf(lambda _: True, lambda _: True)
        self.assertTrue(rule({}))

    def test_fails(self):
        rule = flask_jwt.rules.AllOf(lambda _: True, lambda _: False)
        self.assertFalse(rule({}))
