"""
flask_jwt

example:

    app = flask.Flask(__name__)
    jwt_handler = flask_jwt.FlaskJWT(app)

    @protected(HasScopes('read:some_page'), MatchValue('url:uuid', 'token:uuid'))
    @app.route('/some/page', methods=['GET'])
    def some_page():
        return
"""
from . import handler, protection, rules


# handler stuff...
FlaskJWT = handler.FlaskJWT
current_token = handler.current_token

# protection stuff...
protected = protection.JWTProtected

# protection rules
ProtectionRule = rules.JWTProtectionRule
HasScopes = rules.HasScopes
MatchValue = rules.MatchValue
