import logging

import uvicorn
from fastapi import FastAPI
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


@app.on_event("startup")
async def startup():
    logging.info("initialized connection.")


@app.on_event("shutdown")
async def shutdown():
    logging.info("closed redis connection.")


app.include_router(events.router, prefix="/api/v1/events", tags=["Запись событий"])\

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000,
    )
