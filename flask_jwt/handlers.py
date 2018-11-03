from typing import Any, Dict, List, Optional, Union
import time
import json
import flask
import jwt
from . import errors


class _Store:

    key = "jwt"

    @classmethod
    def set(cls, token: Dict) -> None:
        setattr(flask.g, cls.key, token)

    @classmethod
    def get(cls) -> Union[Dict, None]:
        return getattr(flask.g, cls.key, None)


class _Coder:

    decode_error = errors.JWTDecodeError
    encode_error = errors.JWTEncodeError

    @classmethod
    def decode(
        cls,
        jwt_bytes: bytes,
        secret: str,
        algorithms: List[str],
        verify: bool = True,
        options: Optional[Dict] = None,
        **validate: Any,
    ) -> Dict:
        try:
            return jwt.decode(
                jwt_bytes, secret, verify, algorithms, options, **validate
            )
        except jwt.PyJWTError as ex:
            raise cls.decode_error(ex)

    @classmethod
    def encode(
        cls,
        token: Dict,
        secret: str,
        algorithm: str,
        headers: Optional[Dict] = None,
        json_encoder: Optional[json.JSONEncoder] = None,
    ) -> bytes:
        try:
            return jwt.encode(token, secret, algorithm, headers, json_encoder)
        except jwt.PyJWTError as ex:
            raise cls.encode_error(ex)


class JWTHandler:

    store = _Store
    coder = _Coder
    encoding: str = "utf8"

    def __init__(
        self,
        secret: str,
        lifespan: int,
        algorithm: str = "HS256",
        issuer: Union[str, List[str]] = None,
        audience: Union[str, List[str]] = None,
        json_encoder: Optional[json.JSONEncoder] = None,
    ):
        self.secret = secret
        self.lifespan = lifespan
        self.algorithm = algorithm
        self.issuer = issuer
        self.audience = audience
        self.json_encoder = json_encoder

    def encode(
        self, token: Dict, headers: Optional[Dict] = None, not_before=None
    ) -> str:
        token["exp"] = time.time() + self.lifespan
        if self.issuer and "iss" not in token:
            token["iss"] = self.issuer
        if self.audience and "aud" not in token:
            token["aud"] = self.audience
        if not_before and "nbf" not in token:
            token["nbf"] = not_before
        token_bytes: bytes = self.coder.encode(
            token, self.secret, self.algorithm, headers, self.json_encoder
        )
        return token_bytes.decode(self.encoding)

    def decode(
        self, jwt_string: str, verify: bool = True, options: Optional[Dict] = None
    ) -> Dict:
        token_bytes: bytes = jwt_string.encode(self.encoding)
        return self.coder.decode(
            token_bytes,
            self.secret,
            [self.algorithm],
            verify,
            options,
            issuer=self.issuer,
            audience=self.audience,
        )

    @classmethod
    def current_token(cls) -> Union[Dict, None]:
        return cls.store.get()

    @classmethod
    def generate_token(cls, *scopes: str, **fields: Any) -> None:
        fields["iat"] = time.time()
        fields["scp"] = scopes
        cls.store.set(fields)


class FlaskJWT(JWTHandler):

    header_key = "Authorization"
    token_prefix = "Bearer "

    def __init__(
        self, *args: Any, verify: bool = True, auto_update: bool = False, **kwargs: Any
    ):
        super(FlaskJWT, self).__init__(*args, **kwargs)
        self.verify = verify
        self.auto_update = auto_update
        self.app = None

    def init_app(self, app: flask.Flask) -> None:
        self.app = app
        self.app.before_request(self._pre_request_callback)
        self.app.after_request(self._post_request_callback)

        self.app.errorhandler(errors.JWTDecodeError)(self._handle_user_error)
        self.app.errorhandler(errors.JWTValidationError)(self._handle_user_error)

    @staticmethod
    def _handle_user_error(_: Exception):
        return "invalid token", 403

    def _pre_request_callback(self) -> None:
        prefix = self.token_prefix
        token_string = flask.request.headers.get(self.header_key, None)
        if token_string:
            if not token_string.startswith(prefix) and len(token_string) > len(prefix):
                raise errors.JWTValidationError("invalid bearer token")
            token_string = token_string[len(prefix) :]
            decoded = self.decode(token_string, self.verify)
            self.store.set(decoded)

    def _post_request_callback(self, response: flask.Response) -> None:
        prefix = self.token_prefix
        if self.auto_update:
            token_dict = self.store.get()
            if token_dict:
                encoded = self.encode(token_dict)
                response.headers.set(self.header_key, f"{prefix}{encoded}")
        return response
