from fastapi import FastAPI
from services.auth.routers import auth
from common.config import settings
import os
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

app = FastAPI(title="ecofarm-auth", version="0.1.0")

# Initialize Sentry if DSN provided
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENV,
        release=settings.SENTRY_RELEASE,
        traces_sample_rate=0.05,
    )
    app.add_middleware(SentryAsgiMiddleware)

app.include_router(auth.router, prefix="/auth", tags=["auth"]) 

@app.get("/")
async def root():
    return {"status": "auth service up"}

@app.get("/healthz", tags=["health"])
async def healthz():
    return {"status": "ok"}
