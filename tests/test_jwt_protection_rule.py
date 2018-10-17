import unittest
from flask_jwt import rules


class JWTProtectionRuleTest(unittest.TestCase):
    def test_raises_error_when_implemented_directly(self):
        token = {}
        rule = rules.JWTProtectionRule()
        self.assertRaises(NotImplementedError, rule, token)
