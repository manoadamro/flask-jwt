"""
flask_jwt

example:

    from flask import Flask
    from flask_jwt import JWTHandler, JWTGenerator, jwt_protected, HasScopes, MatchValue, AnyOf

    app = Flask(__name__)

    jwt_handler = JWTHandler('secret')
    jwt_handler.init_app(app)

    jwt_generator = JWTGenerator('my_issuer', ['audience_1', 'audience_2'])


    @app.route('/<uid>/token')
    def auth(uid):
        jwt_generator.generate(['read:thing', 'write:thing'], uid=uid)
        ...


    @app.route('/<user_id>/thing')
    @jwt_protected(HasScopes('read:thing', 'write:thing'))
    def thing(user_id):
        ...


    @app.route('/<uid>/other')
    @jwt_protected(MatchValue('token:uid', 'url:uid'))
    def other(uid):
        ...


    @app.route('/<user_id>/thing')
    @jwt_protected(AnyOf(HasScopes('read:thing', 'write:thing'), MatchValue('token:uid', 'url:uid')))
    def mix(user_id):
        ...
"""
from . import handler, generator, protection, rules


# handler stuff...
JWTHandler = handler.JWTHandler
current_token = handler.current_token

# generator stuff...
JWTGenerator = generator.JWTGenerator

# protection stuff...
jwt_protected = protection.JWTProtected

# protection rules...
ProtectionRule = rules.JWTProtectionRule
HasScopes = rules.HasScopes
MatchValue = rules.MatchValue
AnyOf = rules.AnyOf

# errors...
JWTError = handler.FlaskJWTError
JWTRuleError = rules.JWTRuleError
JWTValidationError = handler.FlaskJWTValidationError
