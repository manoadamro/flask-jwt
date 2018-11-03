import unittest
import flask_jwt


class HasScopesTest(unittest.TestCase):
    def test_has_scopes(self):
        token = {"scp": ["read:thing", "write:thing"]}
        rule = flask_jwt.rules.HasScopes("read:thing", "write:thing")
        self.assertTrue(rule(token))

    def test_has_scopes_fails(self):
        token = {"scp": ["read:thing"]}
        rule = flask_jwt.rules.HasScopes("read:thing", "write:thing")
        self.assertFalse(rule(token))
