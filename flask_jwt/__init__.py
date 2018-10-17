"""
flask_jwt

"""
from . import handler, protection

# handler stuff...
FlaskJWT = handler.FlaskJWT
current_token = handler.current_token

# protection stuff...
protected = protection.JWTProtected
ProtectionRule = protection.JWTProtectionRule
HasScopes = protection.HasScopes
