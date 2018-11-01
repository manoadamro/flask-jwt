import unittest
import time
import flask_jwt
from . import mocks


class TestJWTHandler(unittest.TestCase):
    def setUp(self):
        self.store = flask_jwt._Store

    def test_encode_decode(self):
        handler = flask_jwt._Handler(
            "secret", 15 * 60, issuer="thing", audience="thingy"
        )
        token = {"thing": True}
        encoded = handler.encode(token, not_before=time.time())
        self.assertIsInstance(encoded, str)
        decoded = handler.decode(encoded)
        self.assertIsInstance(decoded, dict)
        self.assertEqual(len(token), len(decoded))
        for key in token:
            self.assertTrue(key in decoded)
            self.assertEqual(decoded[key], token[key])

    def test_current_token(self):
        token = {"thing": True}
        mock = mocks.MockStore(token)
        with mocks.patch_object(flask_jwt.FlaskJWT, "store", mock):
            obj = flask_jwt.FlaskJWT.current_token()
            self.assertEqual(len(token), len(obj))
            for key in token:
                self.assertTrue(key in obj)
                self.assertEqual(token[key], obj[key])

    def test_generate_token(self):
        token = {"thing": True}
        default = ["iat"]
        mock = mocks.MockStore(token)
        with mocks.patch_object(flask_jwt.FlaskJWT, "store", mock):
            flask_jwt.FlaskJWT.generate_token(**{"thing": True})
            self.assertEqual(len(token) + len(default), len(mock.obj))
            for key in token:
                self.assertTrue(key in mock.obj)
                self.assertEqual(token[key], mock.obj[key])
