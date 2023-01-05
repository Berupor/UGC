import logging
from http import HTTPStatus

import jwt
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse

from api.v1 import events
from core.config import Config

config = Config()

app = FastAPI(
    title="API для получения и обработки данных пользовательского поведения",
    description="Информация о событиях и действиях пользователей",
    version="1.0.0",
    docs_url="/ugc/api/openapi",
    openapi_url="/ugc/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if app.docs_url in request.url.path:
        response = await call_next(request)
        return response
    if request.cookies.get("access_token_cookie"):
        payload = jwt.decode(
            request.cookies.get("access_token_cookie"),
            config.secret_key,
            config.token_algo,
        )
        request.state.id_user = payload.get("user_id")
        response = await call_next(request)
        return response
    return Response(status_code=HTTPStatus.UNAUTHORIZED, content="access is denied")


@app.on_event("startup")
async def startup():
    logging.info("initialized connection.")


@app.on_event("shutdown")
async def shutdown():
    logging.info("closed redis connection.")


app.include_router(events.router, prefix="/api/v1/events", tags=["Запись событий"])
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
