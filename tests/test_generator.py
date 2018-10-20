import unittest
import time
import flask
from flask_jwt import generator, handler


class GeneratorTest(unittest.TestCase):
    def test_generate(self):
        app = flask.Flask(__name__)
        iss = "some_issuer"
        aud = ["aud1", "aud2"]
        scopes = ["read:thing", "write:thing"]
        gen = generator.JWTGenerator(iss, aud)
        with app.app_context():
            gen.generate(scopes, not_before=time.time() + 300)
            token = flask.g[handler._G_KEY]
        self.assertIsNotNone(token)
        self.assertEqual(token.get("iss"), iss)
        self.assertEqual(token.get("aud"), aud)
        self.assertEqual(token.get("scopes"), scopes)
        self.assertIsNotNone(token.get("nbf"))
