"""
protection.py

"""
from typing import Any, Callable
import functools
from . import handler, rules


class JWTProtected:
    """
    decorator for protecting methods
    looks for a token in flasks g (using current_token)
    if no token exists or the token does not pass validation,
    a JWTRuleError is raised
    """

    def __init__(self, *jwt_rules: rules.JWTProtectionRule):
        """
        creates an instance of JWTProtected

        :param rules: a tuple of rule objects
        """
        self.rules = jwt_rules

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
            token: dict = handler.current_token()
            if not token:
                raise rules.JWTRuleError("client did not supply a token")
            if not self.validate(token):
                raise rules.JWTRuleError(
                    "one or more jwt protection rules were violated"
                )
            return func(*args, **kwargs)

        return wrapped
