from fastapi import FastAPI
from services.ai_recs.routers import recs
from common.config import settings
import os
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

app = FastAPI(title="ecofarm-ai-recs", version="0.1.0")

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENV,
        release=settings.SENTRY_RELEASE,
        traces_sample_rate=0.05,
    )
    app.add_middleware(SentryAsgiMiddleware)

app.include_router(recs.router, prefix="/ai/rec", tags=["ai_recs"]) 

@app.get("/")
async def root():
    return {"status": "ai_recs service up"}

@app.get("/healthz", tags=["health"])
async def healthz():
    return {"status": "ok"}
