import unittest
import flask
import flask_jwt


class CurrentTokenTest(unittest.TestCase):
    def test_returns_from_g_when_exists(self):
        g_key = flask_jwt._G_KEY
        fake_g = {"thing": True, "other": 22, g_key: {"some": "token"}}
        flask.g = fake_g
        self.assertEqual(flask_jwt.current_token(), fake_g[g_key])

    def test_returns_none_when_not_exists(self):
        fake_g = {"thing": True, "other": 22}
        flask.g = fake_g
        self.assertIsNone(flask_jwt.current_token())

    def test_raises_error_with_no_app_context(self):
        self.assertRaises(RuntimeError, flask_jwt.current_token)

    def test_returns_with_app_context(self):
        app = flask.Flask(__name__)
        with app.app_context():
            self.assertIsNone(flask_jwt.current_token())
