import unittest
import flask
from flask_jwt import handler


class CurrentTokenTest(unittest.TestCase):
    def test_returns_from_g_when_exists(self):
        g_key = handler._G_KEY
        fake_g = {"thing": True, "other": 22, g_key: {"some": "token"}}
        flask.g = fake_g
        self.assertEqual(handler.current_token(), fake_g[g_key])

    def test_returns_none_when_not_exists(self):
        fake_g = {"thing": True, "other": 22}
        flask.g = fake_g
        self.assertIsNone(handler.current_token())

    def test_raises_error_with_no_app_context(self):
        self.assertRaises(RuntimeError, handler.current_token)

    def test_returns_with_app_context(self):
        app = flask.Flask(__name__)
        with app.app_context():
            self.assertIsNone(handler.current_token())
