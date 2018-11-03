import unittest
import flask_jwt


class MatchValueTest(unittest.TestCase):
    def test_invalid_object(self):
        paths = "nope:uuid", "jwt:uuid"
        self.assertRaises(AttributeError, flask_jwt.rules.MatchValue, *paths)

    def test_single_path(self):
        path = "jwt:uuid"
        self.assertRaises(ValueError, flask_jwt.rules.MatchValue, path)
