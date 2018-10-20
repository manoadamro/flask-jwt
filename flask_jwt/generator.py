"""
generator.py

"""
from typing import Union, List, Any
import time
import flask
from . import handler


class JWTGenerator:
    """
    generates tokens for a given issuer and audience

    example:

        token_generator = flask_jwt.JWTGenerator('issuer1', ['audience1', 'audience2'])
        token_generator.generate(scopes=['read:thing', 'write:thing'])

    """

    def __init__(
        self,
        issuer: Union[str, List[str]] = None,
        audience: Union[str, List[str]] = None,
    ):
        """
        creates an instance of _JWTGenerator for generating tokens for a specified audience,
        and from s specified issuer

        :param issuer: token issuer (iss)
        :param audience: token audience (aud)
        """
        self.issuer = issuer
        self.audience = audience

    def generate(
        self, scopes: List[str] = None, not_before: float = None, **kwargs: Any
    ) -> None:
        """
        generates a new jwt with specified fields and stores in g
        iat and exp are auto populated

        :param scopes: list of scopes
        :param not_before: raises an error if validated before stated time
        :param kwargs: custom fields
        :return: no return behaviour
        """
        kwargs["scopes"] = scopes or []
        kwargs["iat"] = time.time()

        if self.issuer:
            kwargs["iss"] = self.issuer

        if self.audience:
            kwargs["aud"] = self.audience

        if not_before is not None:
            kwargs["nbf"] = not_before

        flask.g[handler._G_KEY] = kwargs
