from dataclasses import dataclass


class ApiException(Exception):
    pass


@dataclass
class BadRequestException(ApiException):
    message: str = "Invalid request data"
    extra_information: str = "None"
    code: str = "B001"


class AuthTokenMissedException(ApiException):
    message: str = "Bearer token has not been provided"
    code: str = "A001"


class AuthTokenOutdatedException(ApiException):
    message: str = "Token is outdated"
    code: str = "A002"


class AuthTokenInvalidAudience(ApiException):
    message: str = "Invalid token audience"
    code: str = "A003"


class AuthTokenWithWrongSignatureException(ApiException):
    message: str = "Token with wrong signature"
    code: str = "A004"


class AuthTokenInvalidScheme(ApiException):
    message: str = "Invalid authentication scheme"
    code: str = "A005"


class AuthTokenExpiredException(ApiException):
    message: str = "Expired token"
    code: str = "A006"
