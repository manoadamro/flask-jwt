"""
rules.py

"""
from typing import Dict
import jwt


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
