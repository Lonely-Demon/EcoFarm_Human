# Logging Usage Guide

## Quick Start

Use the centralized logging config in your FastAPI services.

### Example: In `services/farms/main.py`

```python
from fastapi import FastAPI
from shared.logging_config import setup_logging

# Initialize logger
logger = setup_logging("ecofarm-farms")

app = FastAPI()

@app.on_event("startup")
def startup():
    logger.info("Farms service started")

@app.get("/health")
def health():
    logger.debug("Health check called")
    return {"status": "ok"}

@app.post("/farms")
def create_farm(name: str):
    logger.info(f"Creating farm: {name}")
    try:
        # Your logic here
        logger.info(f"Farm created successfully: {name}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Failed to create farm: {e}", exc_info=True)
        return {"error": str(e)}
```

## Environment Variables

Set these on Render for each service:

```
# Axiom logging (current)
AXIOM_API_TOKEN = xaat_...       # Your Axiom token
AXIOM_DATASET = ecofarm           # Dataset name
LOGGING_BACKEND = axiom           # Use Axiom (default)

# Optional: For future Loki migration
LOKI_URL = http://localhost:3100  # Not needed yet, but supports future migration
```

## Switching to Loki (Future)

When you're ready to self-host Loki, just change:

```
LOGGING_BACKEND = loki
LOKI_URL = https://your-loki-server.com
```

No code changes needed! The abstraction handles it.

## Log Levels

Use standard Python logging levels:

```python
logger.debug("Detailed debugging info")      # Dev only
logger.info("Normal operation events")       # Default
logger.warning("Something unexpected")       # Warnings
logger.error("Error occurred", exc_info=True) # Errors with stack trace
logger.critical("Critical failure")          # System critical
```

## Axiom Dashboard

View your logs:
1. Go to https://axiom.co/app
2. Click your dataset: `ecofarm`
3. See all logs from all services

Filter by:
- Service name
- Environment (production/staging)
- Log level
- Time range
- Custom fields

## Notes

- Logs are sent asynchronously (doesn't block your app)
- If Axiom is unreachable, logs still go to console (graceful fallback)
- Production errors are captured with full stack traces
- Each log entry includes service, environment, module, function, and line number
