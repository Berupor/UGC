import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
import jwt

from api.v1 import events
from api.v1.decorators import exception_handler
from core import exceptions
from core.config import settings
from event_streamer.kafka_streamer import kafka_client

app = FastAPI(
    title="API для получения и обработки данных пользовательского поведения",
    description="Информация о событиях и действиях пользователей",
    version="1.0.0",
    docs_url="/ugc/api/openapi",
    openapi_url="/ugc/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.middleware("http")
@exception_handler
async def add_process_time_header(request: Request, call_next):
    if app.docs_url in request.url.path:
        response = await call_next(request)
        return response

    try:
        if request.cookies.get("access_token_cookie"):
            payload = jwt.decode(
                request.cookies.get("access_token_cookie"),
                settings.fastapi.secret_key,
                settings.token_algo,
            )
            request.state.id_user = payload.get("user_id")
            response = await call_next(request)
            return response
        else:
            raise exceptions.AuthTokenMissedException

    except jwt.exceptions.InvalidAudienceError:
        raise exceptions.AuthTokenInvalidAudience
    except jwt.exceptions.ExpiredSignatureError:
        raise exceptions.AuthTokenOutdatedException
    except jwt.exceptions.InvalidSignatureError:
        raise exceptions.AuthTokenWithWrongSignatureException


@app.exception_handler(RequestValidationError)
@exception_handler
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom error message for pydantic error
    """
    # Get the original 'detail' list of errors
    error = exc.errors()[0]
    raise exceptions.BadRequestException(extra_information=error["msg"])


@app.on_event("startup")
async def startup():
    logging.info("initialized connection.")


@app.on_event("shutdown")
async def shutdown():
    await kafka_client.stop_producer()
    await kafka_client.stop_consumer()

    logging.info("closed redis connection.")


app.include_router(events.router, prefix="/api/v1/events", tags=["Запись событий"])
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.fastapi.host,
        port=settings.fastapi.port,
    )
