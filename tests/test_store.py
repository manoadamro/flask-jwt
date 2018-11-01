import unittest
import flask
import flask_jwt
from . import mocks


class TestJWTStore(unittest.TestCase):
    def setUp(self):
        self.store = flask_jwt._Store

    def test_get_set(self):
        fake_g_attrs = {"some": "thing", "other": True}
        with mocks.patch_object(flask, "g", mocks.FakeG()):
            self.store.set(fake_g_attrs)
            for k in fake_g_attrs:
                self.assertTrue(hasattr(flask.g, "jwt"))
                self.assertTrue(k in flask.g.jwt)
                self.assertEqual(flask.g.jwt[k], fake_g_attrs[k])
            token = self.store.get()
            for k in fake_g_attrs:
                self.assertTrue(k in token)
                self.assertEqual(fake_g_attrs[k], token[k])

    def test_returns_none_if_no_token_set(self):
        with mocks.patch_object(flask, "g", mocks.FakeG()):
            self.assertIsNone(self.store.get())
