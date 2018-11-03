import unittest
import flask
import flask_jwt
from .. import mocks


class MatchValueTest(unittest.TestCase):
    def test_invalid_object(self):
        paths = "nope:uuid", "jwt:uuid"
        self.assertRaises(AttributeError, flask_jwt.rules.MatchValue, *paths)

    def test_single_path(self):
        path = "jwt:uuid"
        self.assertRaises(ValueError, flask_jwt.rules.MatchValue, path)

    def test_header(self):
        paths = "header:uuid", "jwt:uuid"
        header = {"uuid": "1234"}
        token = {"uuid": "1234"}
        rule = flask_jwt.rules.MatchValue(*paths)
        with mocks.patch_object(flask, "request", mocks.MockRequest(headers=header)):
            self.assertTrue(rule(token))

    def test_header_fails(self):
        paths = "header:uuid", "jwt:uuid"
        header = {"uuid": "1234"}
        token = {"uuid": "4321"}
        rule = flask_jwt.rules.MatchValue(*paths)
        with mocks.patch_object(flask, "request", mocks.MockRequest(headers=header)):
            self.assertFalse(rule(token))

    def test_json(self):
        paths = "json:user/uuid", "jwt:uuid"
        json = {"user": {"uuid": "1234"}}
        token = {"uuid": "1234"}
        rule = flask_jwt.rules.MatchValue(*paths)
        with mocks.patch_object(flask, "request", mocks.MockRequest(json=json)):
            self.assertTrue(rule(token))

    def test_json_fails(self):
        paths = "json:user/uuid", "jwt:uuid"
        json = {"user": {"uuid": "4321"}}
        token = {"uuid": "1234"}
        rule = flask_jwt.rules.MatchValue(*paths)
        with mocks.patch_object(flask, "request", mocks.MockRequest(json=json)):
            self.assertFalse(rule(token))

    def test_url(self):
        paths = "url:uuid", "jwt:uuid"
        view_args = {"uuid": "1234"}
        token = {"uuid": "1234"}
        rule = flask_jwt.rules.MatchValue(*paths)
        with mocks.patch_object(
            flask, "request", mocks.MockRequest(view_args=view_args)
        ):
            self.assertTrue(rule(token))

    def test_url_fails(self):
        paths = "url:uuid", "jwt:uuid"
        view_args = {"uuid": "1234"}
        token = {"uuid": "4321"}
        rule = flask_jwt.rules.MatchValue(*paths)
        with mocks.patch_object(
            flask, "request", mocks.MockRequest(view_args=view_args)
        ):
            self.assertFalse(rule(token))

    def test_param(self):
        paths = "param:uuid", "jwt:uuid"
        args = {"uuid": "1234"}
        token = {"uuid": "1234"}
        rule = flask_jwt.rules.MatchValue(*paths)
        with mocks.patch_object(flask, "request", mocks.MockRequest(args=args)):
            self.assertTrue(rule(token))

    def test_param_fails(self):
        paths = "param:uuid", "jwt:uuid"
        args = {"uuid": "1234"}
        token = {"uuid": "4321"}
        rule = flask_jwt.rules.MatchValue(*paths)
        with mocks.patch_object(flask, "request", mocks.MockRequest(args=args)):
            self.assertFalse(rule(token))

    def test_form(self):
        paths = "form:uuid", "jwt:uuid"
        form = {"uuid": "1234"}
        token = {"uuid": "1234"}
        rule = flask_jwt.rules.MatchValue(*paths)
        with mocks.patch_object(flask, "request", mocks.MockRequest(form=form)):
            self.assertTrue(rule(token))

    def test_form_fails(self):
        paths = "form:uuid", "jwt:uuid"
        form = {"uuid": "1234"}
        token = {"uuid": "4321"}
        rule = flask_jwt.rules.MatchValue(*paths)
        with mocks.patch_object(flask, "request", mocks.MockRequest(form=form)):
            self.assertFalse(rule(token))
