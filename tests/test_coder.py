import unittest
import jwt
import flask_jwt
from . import mocks


class JWTCoderTest(unittest.TestCase):
    fake_jwt = {"some": "thing"}

    def setUp(self):
        self.coder = flask_jwt.handlers._Coder

    def test_get_set(self):
        token = self.coder.encode(self.fake_jwt, "secret", "HS256")
        self.assertIsInstance(token, bytes)
        decoded = self.coder.decode(token, "secret", ["HS256"], verify=False)
        self.assertEqual(len(decoded), len(self.fake_jwt))
        for key in self.fake_jwt:
            self.assertEqual(self.fake_jwt[key], decoded[key])

    def test_encode_error(self):
        with mocks.patch_object(
            jwt, "encode", mocks.raise_error(flask_jwt.errors.JWTEncodeError)
        ):
            self.assertRaises(
                flask_jwt.errors.JWTEncodeError,
                self.coder.encode,
                self.fake_jwt,
                "secret",
                "HS256",
            )

    def test_decode_error(self):
        with mocks.patch_object(
            jwt, "decode", mocks.raise_error(flask_jwt.errors.JWTDecodeError)
        ):
            self.assertRaises(
                flask_jwt.errors.JWTDecodeError,
                self.coder.decode,
                self.fake_jwt,
                "secret",
                "HS256",
            )
