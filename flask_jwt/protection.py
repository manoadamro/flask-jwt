"""
protection.py

"""
from typing import Any, Dict, Callable
import functools
import jwt
from .handler import current_token


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


class JWTProtected:
    """
    decorator for protecting methods
    looks for a token in flasks g (using current_token)
    if no token exists or the token does not pass validation,
    a JWTRuleError is raised
    """

    def __init__(self, *rules: JWTProtectionRule):
        """
        creates an instance of JWTProtected

        :param rules: a tuple of rule objects
        """
        self.rules = rules

    def validate(self, token: dict) -> bool:
        """
        checks the token against all the rules

        :param token: token from current request headers
        :return: True if the token adheres to all the rules
        """
        return all(rule(token) for rule in self.rules)

    def __call__(self, func: Callable) -> Callable:
        """
        called when decorated function is registered

        :param func: decorated function
        :return: callable func wrapper
        """

        @functools.wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Callable:
            """
            validates a token against the specified tuple of rules
            if any rules are not met, a JWTRuleError is raised
            if all rules are met, the decorated function is called and its return value is forwarded

            :param args: args passed to decorated function
            :param kwargs: kargs passed to decorated function
            :return: whatever is returned from decorated function
            """
            token = current_token()
            if not token:
                raise JWTRuleError("client did not supply a token")
            if not self.validate(token):
                raise JWTRuleError("one or more jwt protection rules were violated")
            return func(*args, **kwargs)

        return wrapped


class HasScopes(JWTProtectionRule):
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
        jwt_scopes = token.get("scopes", [])
        missing_scopes = [scope for scope in self.scopes if scope not in jwt_scopes]
        if missing_scopes:
            missing_scopes = ", ".join(missing_scopes)
            raise JWTRuleError(f"jwt is missing a required scope {missing_scopes}")
        return True
