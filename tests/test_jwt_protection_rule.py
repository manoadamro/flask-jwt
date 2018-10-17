import unittest
from flask_jwt import protection


class JWTProtectionRuleTest(unittest.TestCase):
    def test_raises_error_when_implemented_directly(self):
        token = {}
        rule = protection.JWTProtectionRule()
        self.assertRaises(NotImplementedError, rule, token)
