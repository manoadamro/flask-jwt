"""
rules.py

"""
from typing import Dict, Any, List, Callable
import jsonpointer
import flask
import jwt
from . import handler


class JWTRuleError(jwt.PyJWTError):
    """
    raised when one or more jwt protection rules fail
    """

    ...


class JWTProtectionRule:
    """
    base class for jwt protection rules

    example:

    class HasKey(JWTProtectionRule):

        def __init__(self, key):
            self.key = key

        def __call__(self, token):
            return self.key in token
    """

    def __call__(self, token: Dict) -> bool:
        """
        called by JWTProtected decorator

        :param token: token from current request headers
        :return: True if rules are met else False
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} should not be implemented directly"
        )


class HasScopes(JWTProtectionRule):
    """
    checks that a jwt contains all of the defined scopes

    example:

        @JWTProtected(HasScopes('read:thing', 'write:thing'))
        def some_method():
            ...
    """

    def __init__(self, *scopes: str):
        """
        ensures that the current jwt contains all of the specified scopes
        scopes are usually defined with an operation followed by an object, separated by a colon

        example:
            read:the_thing
            write:the_thing

        :param scopes: list of scopes (strings)
        """
        self.scopes = scopes

    def __call__(self, token: Dict) -> bool:
        """
        called by JWTProtected decorator when validating a token

        :param token: token from current request headers
        :return: True if rules are met else False
        """
        jwt_scopes: list = token.get("scopes", [])
        missing_scopes: list = [
            scope for scope in self.scopes if scope not in jwt_scopes
        ]
        if missing_scopes:
            missing_scopes: str = ", ".join(missing_scopes)
            raise JWTRuleError(f"jwt is missing a required scope {missing_scopes}")
        return True


class MatchValue(JWTProtectionRule):
    """
    matches a value in the jwt with a value in the request

    example:

        @JWTProtected(MatchValue('json:thing/sub_thing', 'jwt:thingy'))
        def some_method():
            ...
    """

    def __init__(self, *paths):
        """
        creates an instance of MatchValue

        :param paths: a tuple of json pointers
        """
        self.paths = paths

    def __call__(self, token: Dict) -> bool:
        """
        called by JWTProtected decorator when validating a token

        :param token: token from current request headers
        :return: True if rules are met else False
        """
        values: List[Any] = [self._resolve_path(path) for path in self.paths]
        return self._check_equal(values)

    def _resolve_path(self, path: str) -> Any:
        """
        returns a value from a json pointer

        :param path: object name and json pointer separated with ':'
        :return: value at pointer
        """
        object_name, pointer = path.split(":")
        if not pointer.startswith("/"):
            pointer = f"/{pointer}"
        if object_name.startswith("_") or not hasattr(self, object_name):
            raise AttributeError(f"invalid match object {object_name}")
        obj: Callable = getattr(self, object_name)
        try:
            return obj(pointer)
        except jsonpointer.JsonPointerException as ex:
            raise JWTRuleError(ex)

    @staticmethod
    def _check_equal(values: List[Any]) -> bool:
        """
        checks that every value in a given list is identical

        :param values: the list of values to check
        :return: True if every value in the list is identical
        """
        if len(values) < 2:
            return True
        return all(values[0] == rest for rest in values[1:])

    @staticmethod
    def header(path: str) -> Any:
        """
        returns a value from the request header from a json pointer

        :param path: object name and json pointer separated with ':'
        :return: value at pointer
        """
        return jsonpointer.resolve_pointer(flask.request.headers, path)

    @staticmethod
    def json(path: str) -> Any:
        """
        returns a value from the request json from a json pointer

        :param path: object name and json pointer separated with ':'
        :return: value at pointer
        """
        return jsonpointer.resolve_pointer(flask.request.json, path)

    @staticmethod
    def url(path: str) -> Any:
        """
        returns a value from the url from a json pointer

        :param path: object name and json pointer separated with ':'
        :return: value at pointer
        """
        return jsonpointer.resolve_pointer(flask.request.view_args, path)

    @staticmethod
    def param(path: str) -> Any:
        """
        returns a value from a url parameter from a json pointer

        :param path: object name and json pointer separated with ':'
        :return: value at pointer
        """
        return jsonpointer.resolve_pointer(flask.request.args, path)

    @staticmethod
    def form(path: str) -> Any:
        """
        returns a value from the request form from a json pointer

        :param path: object name and json pointer separated with ':'
        :return: value at pointer
        """
        return jsonpointer.resolve_pointer(flask.request.form, path)

    @staticmethod
    def jwt(path: str) -> Any:
        """
        returns a value from the request jwt from a json pointer

        :param path: object name and json pointer separated with ':'
        :return: value at pointer
        """
        return jsonpointer.resolve_pointer(handler.current_token(), path)
