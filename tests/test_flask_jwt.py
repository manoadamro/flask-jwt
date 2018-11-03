import unittest
import jwt
import flask
import flask_jwt
from . import mocks


class FlaskJWTTest(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)
        self.flaskjwt = flask_jwt.handlers.FlaskJWT("secret", 60)
        self.flaskjwt.init_app(self.app)

    def test_no_token(self):
        mock_store = mocks.MockStore()
        mock_request = mocks.MockRequest(headers={})
        with mocks.patch_object(flask, "request", mock_request), mocks.patch_object(
            flask_jwt.handlers.FlaskJWT, "store", mock_store
        ):
            self.flaskjwt._pre_request_callback()
            self.assertEqual(mock_store.obj, {})
            response = flask.Response(200)
            self.flaskjwt._post_request_callback(response)
            auth = response.headers.get("Authorization")
            self.assertIsNone(auth)

    def test_with_token(self):
        token_body = {"thing": True}
        token = jwt.encode(token_body, "secret").decode("utf8")
        mock_store = mocks.MockStore()
        mock_request = mocks.MockRequest(headers={"Authorization": token})
        with mocks.patch_object(flask, "request", mock_request), mocks.patch_object(
            flask_jwt.handlers.FlaskJWT, "store", mock_store
        ):
            self.flaskjwt._pre_request_callback()
            self.assertEqual(mock_store.obj, token_body)
            response = flask.Response(200)
            self.flaskjwt._post_request_callback(response)
            auth = response.headers.get("Authorization")
            self.assertIsNotNone(auth)
