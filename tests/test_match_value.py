import unittest
import flask
from flask_jwt import protection, handler, rules


@protection.JWTProtected(rules.MatchValue("header:/thing", "jwt:/thingy"))
def fake_method1():
    return True


@protection.JWTProtected(rules.MatchValue("json:/thing/other", "jwt:/thingy"))
def fake_method2():
    return True


@protection.JWTProtected(rules.MatchValue("url:/thing", "jwt:/thingy"))
def fake_method3():
    return True


@protection.JWTProtected(rules.MatchValue("param:/thing", "jwt:/thingy"))
def fake_method4():
    return True


@protection.JWTProtected(rules.MatchValue("form:/thing", "jwt:/thingy"))
def fake_method5():
    return True


@protection.JWTProtected(rules.MatchValue("header:thing", "jwt:thingy"))
def fake_method_no_leading_slash():
    return True


@protection.JWTProtected(rules.MatchValue("nope:/thing", "jwt:/thingy"))
def fake_method_bad_object():
    return True


@protection.JWTProtected(
    rules.MatchValue("header:/thing", "json:/thing/other", "jwt:/thingy")
)
def fake_method_many_values():
    return True


@protection.JWTProtected(rules.MatchValue("jwt:/thingy"))
def fake_method_one_value():
    return True


@protection.JWTProtected(rules.MatchValue("jwt:/thingy/nope"))
def fake_method_bad_pointer():
    return True


class FakeRequest:
    def __init__(self, headers=None, json=None, view_args=None, param=None, form=None):
        self.headers = headers
        self.json = json
        self.view_args = view_args
        self.args = param
        self.form = form


class MatchValueTest(unittest.TestCase):
    def test_match_header(self):
        flask.g = {handler._G_KEY: {"thingy": "thingy"}}
        flask.request = FakeRequest(headers={"thing": "thingy"})
        self.assertTrue(fake_method1())

    def test_match_json(self):
        flask.g = {handler._G_KEY: {"thingy": 123}}
        flask.request = FakeRequest(json={"thing": {"other": 123}})
        self.assertTrue(fake_method2())

    def test_match_url(self):
        flask.g = {handler._G_KEY: {"thingy": "54321"}}
        flask.request = FakeRequest(view_args={"thing": "54321"})
        self.assertTrue(fake_method3())

    def test_match_param(self):
        flask.g = {handler._G_KEY: {"thingy": "true"}}
        flask.request = FakeRequest(param={"thing": "true"})
        self.assertTrue(fake_method4())

    def test_match_form(self):
        flask.g = {handler._G_KEY: {"thingy": "true"}}
        flask.request = FakeRequest(form={"thing": "true"})
        self.assertTrue(fake_method5())

    def test_match_no_leading_slash(self):
        flask.g = {handler._G_KEY: {"thingy": "thingy"}}
        flask.request = FakeRequest(headers={"thing": "thingy"})
        self.assertTrue(fake_method_no_leading_slash())

    def test_invalid_object_name(self):
        flask.g = {handler._G_KEY: {"thingy": "true"}}
        self.assertRaises(AttributeError, fake_method_bad_object)

    def test_invalid_bad_pointer(self):
        flask.g = {handler._G_KEY: {"thingy": "true"}}
        self.assertRaises(rules.JWTRuleError, fake_method_bad_pointer)

    def test_match_many_values(self):
        flask.g = {handler._G_KEY: {"thingy": "54321"}}
        flask.request = FakeRequest(
            headers={"thing": "54321"}, json={"thing": {"other": "54321"}}
        )
        self.assertTrue(fake_method_many_values())

    def test_match_one_value(self):
        flask.g = {handler._G_KEY: {"thingy": "54321"}}
        self.assertTrue(fake_method_one_value())
