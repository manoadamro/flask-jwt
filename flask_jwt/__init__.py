from typing import Union, Dict
import flask

_HEADER_KEY = "Authorization"
_G_KEY = "_JWT"


def current_token() -> Union[Dict, None]:
    """
    gets the JWT associated with the current request as a dict (assuming one was found in the request header)
    None is returned if no JWT was included in the request header
    :return: JWT as a dict or None
    """
    return flask.g.get(_G_KEY, None)
