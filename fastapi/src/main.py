from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.config import settings

app = FastAPI(
    title="Read-only API for UGC service",
    description="Service for monitoring user activity.",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

