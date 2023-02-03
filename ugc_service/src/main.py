import logging

import logstash
import uvicorn
from api.v1 import bookmarks, events, rating, review
from api.v1.utils.decorators import exception_handler
from core import exceptions
from core.config import settings
from core.logger import LOGGING
from event_streamer.connect.create_connections import init_connections
from event_streamer.kafka_streamer import kafka_client
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from logstash_async.handler import AsynchronousLogstashHandler
from motor.motor_asyncio import AsyncIOMotorClient
from services import base_mongo_service

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
    return await call_next(request)


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
    await init_connections()
    base_mongo_service.mongo_client = AsyncIOMotorClient(
        f"mongodb://{settings.mongo.host}:{settings.mongo.port}/"
    )
    # init_ch()
    logger = logging.getLogger("uvicorn.access")
    logger.setLevel(logging.INFO)
    logger.addHandler(
        logstash.LogstashHandler(
            settings.logstash.host, settings.logstash.port, version=1, tags=['ugc']
        )
    )
    logging.info("info", extra={'tags': 'ugc'})


@app.on_event("shutdown")
async def shutdown():
    await kafka_client.stop_producer()
    await kafka_client.stop_consumer()
    base_mongo_service.mongo_client.close()
    logging.info("closed redis connection.")


app.include_router(events.router, prefix="/api/v1/events", tags=["Запись событий"])
app.include_router(review.router, prefix="/api/v1/reviews", tags=["Рецензии"])
app.include_router(rating.router, prefix="/api/v1/rating", tags=["Рейтинг"])
app.include_router(bookmarks.router, prefix="/api/v1/bookmarks", tags=["Закладки"])
if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.fastapi.host, port=settings.fastapi.port, reload=True
    )
