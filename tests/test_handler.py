import unittest
from unittest.mock import patch
import jwt
import flask
from flask_jwt import handler, JWTValidationError


class FakeRequest:

    test_authorization = {"test": "dict"}

    def __init__(self, headers=None):
        self.headers = headers or {handler._HEADER_KEY: self.fake_token()}

    @classmethod
    def fake_token(cls):
        return jwt.encode(cls.test_authorization, "secret", algorithm="HS256").decode(
            "utf8"
        )


class HandlerTest(unittest.TestCase):
    def tearDown(self):
        flask.g = {}

    def test_decodes_token(self):
        app = flask.Flask(__name__)
        token_handler = handler.JWTHandler("secret", algorithm="HS256", lifespan=300)
        token_handler.init_app(app)
        with app.app_context():
            with patch.object(flask, "request", FakeRequest()):
                token_handler._cache_request_token()
                self.assertEqual(
                    flask.g[handler._G_KEY], FakeRequest.test_authorization
                )

    def test_handles_null_request_token(self):
        app = flask.Flask(__name__)
        token_handler = handler.JWTHandler("secret", algorithm="HS256", lifespan=300)
        token_handler.init_app(app)
        with app.app_context():
            with patch.object(flask, "request", FakeRequest(headers={"nope": "nope"})):
                token_handler._cache_request_token()
                self.assertIsNone(flask.g.get(handler._G_KEY))

    def test_encodes_token(self):
        app = flask.Flask(__name__)
        token_handler = handler.JWTHandler("secret", algorithm="HS256", lifespan=300)
        token_handler.init_app(app)
        with app.app_context():
            with patch.object(flask, "request", FakeRequest()):
                response = flask.Response(status=200)
                flask.g[handler._G_KEY] = FakeRequest.test_authorization
                token_handler._append_response_token(response)
                self.assertEqual(
                    response.headers[handler._HEADER_KEY], FakeRequest.fake_token()
                )

    def test_handles_null_response_token(self):
        app = flask.Flask(__name__)
        token_handler = handler.JWTHandler("secret", algorithm="HS256", lifespan=300)
        token_handler.init_app(app)
        with app.app_context():
            response = flask.Response(status=200)
            flask.g = {}
            token_handler._append_response_token(response)
            self.assertIsNone(response.headers.get(handler._HEADER_KEY, None))

    def test_raises_error_when_invalid(self):
        app = flask.Flask(__name__)
        token_handler = handler.JWTHandler(
            "secret", algorithm="HS256", issuer="issuer1"
        )
        token_handler.init_app(app)
        with app.app_context():
            with patch.object(flask, "request", FakeRequest()):
                self.assertRaises(
                    JWTValidationError, token_handler._cache_request_token
                )
