"""
flask_jwt

"""
from . import handler, protection, rules

# handler stuff...
FlaskJWT = handler.FlaskJWT
current_token = handler.current_token

# protection stuff...
protected = protection.JWTProtected

ProtectionRule = rules.JWTProtectionRule
HasScopes = rules.HasScopes
