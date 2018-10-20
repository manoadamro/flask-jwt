"""
handler.py

"""
from typing import Union, Dict, List
import time
import flask
import jwt


# the key associated with the jwt in request/response headers
_HEADER_KEY = "Authorization"

# the key associated with the jwt in flasks g object
_G_KEY = "_JWT"

# encoding for request/response headers
_ENCODING = "utf8"


class FlaskJWTError(jwt.PyJWTError, PermissionError):
    """
    base class for jwt related errors

    """

    ...


class FlaskJWTValidationError(FlaskJWTError):
    """
    raised when one or more jwt claims are wrong

    """

    ...


def current_token() -> Union[Dict, None]:
    """
    gets the JWT associated with the current request as a dict
    None is returned if no JWT was included in the request header

    :return: JWT as a dict or None
    """
    return flask.g.get(_G_KEY, None)


class JWTHandler:
    """
    Handles the encoding and decoding of tokens in flask requests and responses


    example:

        token_handler = flask_jwt.FlaskJWT('secret', algorithm="HS256")
        token_handler.init_app(app)

        @app.route('/auth/<user_id>')
        def auth(user):
            token_handler.generate_jwt(id=user_id)
    """

    def __init__(
        self,
        secret: str,
        algorithm: str = "HS256",
        lifespan: int = None,
        issuer: Union[str, List[str]] = None,
        audience: Union[str, List[str]] = None,
    ):
        """
        creates an instance of FlaskJWT

        :param secret: signing secret
        :param algorithm: signing algorithm
        :param lifespan: lifespan of the token in seconds (<= 0 for indefinite)
        :param issuer: token issuer (iss)
        :param audience: token audience (aud)
        """
        self.secret = secret
        self.algorithm = algorithm
        self.lifespan = lifespan
        self.issuer = issuer
        self.audience = audience

    def init_app(self, app: flask.Flask) -> None:
        """
        registers before and after request methods with app

        :param app: instance of flask.Flask
        :return: no return behaviour
        """
        app.before_request(self._cache_request_token)
        app.after_request(self._append_response_token)

    def _cache_request_token(self) -> None:
        """
        called by flask before the view method is called
        attempts to find a JWT in the headers of the clients request,
        if no JWT is found, g will not be altered

        :return: no return behaviour
        """
        jwt_string: str = flask.request.headers.get(_HEADER_KEY, None)
        if not jwt_string:
            return

        jwt_bytes: bytes = jwt_string.encode(_ENCODING)

        try:
            decoded: str = jwt.decode(
                jwt_bytes,
                self.secret,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
            )

        except jwt.PyJWTError as ex:
            raise FlaskJWTValidationError(ex)

        flask.g[_G_KEY] = decoded

    def _append_response_token(self, response: flask.Response) -> None:
        """
        called by flask before the response is returned to the client
        if a JWT is stored in g, it will be returned in the response headers
        if no JWT is found, the headers will not be altered

        :param response: flask Response instance, returned from the view method
        :return: no return behaviour
        """

        jwt_object: dict = flask.g.get(_G_KEY, None)
        if not jwt_object:
            return

        if self.lifespan:
            jwt_object["exp"] = time.time() + self.lifespan

        encoded: bytes = jwt.encode(jwt_object, self.secret, self.algorithm)
        decoded: str = encoded.decode(_ENCODING)
        response.headers[_HEADER_KEY] = decoded
