import flask_testing
from flask import Flask, Blueprint
from flask_jwt import FlaskJWT, jwt_protected, HasScopes, MatchValue, generate_token


blueprint = Blueprint("test_blueprint", __name__)


@blueprint.route("/token", methods=["GET"])
def get_token():
    print("/token")
    generate_token("read:protected", uuid="123")
    return "success"


@blueprint.route("/protected", methods=["GET"])
@jwt_protected(HasScopes("read:protected"))
def protected():
    print("/protected")
    return "success"


@blueprint.route("/protected/<uuid>", methods=["GET"])
@jwt_protected(HasScopes("read:protected"), MatchValue("jwt:uuid", "url:uuid"))
def protected_user(uuid):
    print(f"/protected/{uuid}")
    return uuid


class TestApi(flask_testing.TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.register_blueprint(blueprint)
        jwt = FlaskJWT("secret", 300, auto_update=True)
        jwt.init_app(app)
        return app

    def test_run(self):

        auth_key = "Authorization"
        self.assert403(self.client.get("/protected"))
        self.assert403(self.client.get("/protected/123"))

        token_response = self.client.get("/token")
        self.assert200(token_response)
        token = token_response.headers.get(auth_key, None)
        self.assertIsNotNone(token)

        protected_response = self.client.get("/protected", headers={auth_key: token})
        self.assert200(protected_response)
        token = protected_response.headers.get(auth_key, None)
        self.assertIsNotNone(token)

        protected_user_response = self.client.get(
            "/protected/123", headers={auth_key: token}
        )
        self.assert200(protected_user_response)
        token = protected_user_response.headers.get(auth_key, None)
        self.assertIsNotNone(token)

        protected_user_response = self.client.get(
            "/protected/321", headers={auth_key: token}
        )
        self.assert403(protected_user_response)
