import unittest
import jwt
import flask
from flask_jwt import handler


class FakeRequest:

    test_authorization = {"test": "dict"}

    def __init__(self):
        self.headers = {handler._HEADER_KEY: self.fake_token()}

    @classmethod
    def fake_token(cls):
        return jwt.encode(cls.test_authorization, "secret", algorithm="HS256")


class FlaskJWTTest(unittest.TestCase):
    def setUp(self):
        self.real_request = flask.request
        flask.request = FakeRequest()

    def tearDown(self):
        flask.request = self.real_request

    def test_decodes_token(self):
        app = flask.Flask(__name__)
        token_handler = handler.FlaskJWT("secret", algorithm="HS256")
        token_handler.init_app(app)
        with app.app_context():
            token_handler._cache_request_token()
            self.assertEqual(flask.g[handler._G_KEY], FakeRequest.test_authorization)

    def test_encodes_token(self):
        app = flask.Flask(__name__)
        token_handler = handler.FlaskJWT("secret", algorithm="HS256")
        token_handler.init_app(app)
        with app.app_context():
            response = flask.Response(status=200)
            flask.g[handler._G_KEY] = FakeRequest.test_authorization
            token_handler._append_response_token(response)
            self.assertEqual(
                response.headers[handler._HEADER_KEY],
                FakeRequest.fake_token().decode("utf8"),
            )
