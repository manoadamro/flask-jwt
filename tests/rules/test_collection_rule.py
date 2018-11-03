import unittest
import flask_jwt


class CollectionRuleTest(unittest.TestCase):
    def test_fails(self):
        rule = flask_jwt.rules._CollectionRule()
        self.assertRaises(NotImplementedError, rule, "token")
