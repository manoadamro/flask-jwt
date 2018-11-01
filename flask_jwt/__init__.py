from typing import Any, Dict, List, Optional, Union
import time
import json
import flask
import jwt


class FlaskJWTError(jwt.PyJWTError, PermissionError):
    ...


class JWTDecodeError(FlaskJWTError):
    ...


class JWTEncodeError(FlaskJWTError):
    ...


class _Store:

    key = "jwt"

    @classmethod
    def set(cls, token: Dict) -> None:
        setattr(flask.g, cls.key, token)

    @classmethod
    def get(cls) -> Union[Dict, None]:
        return getattr(flask.g, cls.key, None)


class _Coder:

    decode_error = JWTDecodeError
    encode_error = JWTEncodeError

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


class _Handler:

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
    def generate_token(cls, **fields: Any) -> None:
        fields["iat"] = time.time()
        cls.store.set(fields)


class FlaskJWT(_Handler):

    header_key = "Authorization"

    def __init__(self, verify=True, **kwargs: Any):
        super(FlaskJWT, self).__init__(**kwargs)
        self.verify = verify
        self.app = None

    def init_app(self, app: flask.Flask) -> None:
        self.app = app
        self.app.before_request(self._pre_request_callback)
        self.app.after_request(self._pre_request_callback)

    def _pre_request_callback(self):
        token_string = flask.request.headers.get(self.header_key, None)
        if not token_string:
            return
        decoded = self.decode(token_string, self.verify)
        self.store.set(decoded)

    def _post_request_callback(self, response):
        token_dict = self.store.get()
        if not token_dict:
            return
        encoded = self.encode(token_dict)
        response.headers.set(self.header_key, encoded)
