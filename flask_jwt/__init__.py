from . import errors, handlers, rules, decorators


FlaskJWT = handlers.FlaskJWT

current_token = property(fget=handlers.JWTHandler.current_token)
generate_token = handlers.JWTHandler.generate_token

jwt_protected = decorators.JWTProtected

JWTRule = rules.JWTRule
HasScopes = rules.HasScopes
MatchValue = rules.MatchValue
AllOf = rules.AllOf
AnyOf = rules.AnyOf
NoneOf = rules.NoneOf

JWTEncodeError = errors.JWTEncodeError
JWTDecodeError = errors.JWTDecodeError
JWTValidationError = errors.JWTValidationError
