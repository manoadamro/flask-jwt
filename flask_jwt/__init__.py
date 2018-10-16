"""
flask_jwt

"""
from typing import Union, Dict, None
import flask
import jwt


_HEADER_KEY = "Authorization"
_G_KEY = "_JWT"


def current_token() -> Union[Dict, None]:
    """
    gets the JWT associated with the current request as a dict
    None is returned if no JWT was included in the request header

    :return: JWT as a dict or None
    """
    return flask.g.get(_G_KEY, None)


class FlaskJWT:
    """
    Handles the encoding and decoding of tokens in flask requests and responses


    example:

        token_handler = flask_jwt.FlaskJWT('secret', algorithm="HS256")
        token_handler.init_app(app)

    """

    def __init__(self, secret, algorithm="HS256"):
        """
        creates an instance of FlaskJWT

        :param app: instance of flask.Flask
        :param secret:
        :param algorithm:
        """
        self.secret = secret
        self.algorithm = algorithm

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
        jwt_string = flask.request.headers.get(_HEADER_KEY, None)
        if jwt_string:
            decoded = jwt.decode(jwt_string, self.secret, algorithms=[self.algorithm])
            flask.g[_G_KEY] = decoded

    def _append_response_token(self, response: flask.Response) -> None:
        """
        called by flask before the response is returned to the client
        if a JWT is stored in g, it will be returned in the response headers
        if no JWT is found, the headers will not be altered

        :param response: flask Response instance, returned from the view method
        :return: no return behaviour
        """
        jwt_object = flask.g.get(_G_KEY, None)
        if jwt_object:
            encoded = jwt.encode(jwt_object, self.secret, self.algorithm)
            response.headers[_HEADER_KEY] = encoded
