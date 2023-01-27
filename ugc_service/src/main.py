import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

# from api.v1 import events, review, rating, bookmarks
from api.v1 import events, rating, bookmarks
from api.v1.decorators import exception_handler
from core import exceptions
from core.config import settings
from db.clickhouse.migrator import init_ch
from event_streamer.kafka_streamer import kafka_client
from event_streamer.connect.create_connections import init_connections

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
    # init_ch()
    logging.info("initialized connection.")


@app.on_event("shutdown")
async def shutdown():
    await kafka_client.stop_producer()
    await kafka_client.stop_consumer()

    logging.info("closed redis connection.")


app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])
# app.include_router(review.router, prefix="/api/v1/reviews", tags=["Review"])
app.include_router(rating.router, prefix="/api/v1/rating", tags=["Rating"])
app.include_router(bookmarks.router, prefix="/api/v1/bookmarks", tags=["Bookmarks"])
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.fastapi.host,
        port=settings.fastapi.port,
        reload=True
    )
