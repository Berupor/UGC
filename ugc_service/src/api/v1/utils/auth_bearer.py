import time
from typing import List

import jwt  # type: ignore
from core import exceptions
from core.config import settings
from fastapi import Request
from fastapi.security import HTTPBearer


def decode_and_verify_jwt(token: str, secret_key: str, algorithms: List[str]) -> dict:
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=algorithms)
        if decoded_token["exp"] >= time.time():
            return decoded_token

        else:
            raise exceptions.AuthTokenExpiredException
    except jwt.exceptions.DecodeError:
        raise exceptions.AuthTokenWithWrongSignatureException
    except jwt.exceptions.ExpiredSignatureError:
        raise exceptions.AuthTokenExpiredException


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise exceptions.AuthTokenInvalidScheme

            user_id = decode_and_verify_jwt(
                credentials.credentials,
                settings.fastapi.secret_key,
                [settings.token_algo],
            )["user_id"]

            return user_id
