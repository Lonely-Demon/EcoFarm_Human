# Using Axiom Logging in EcoFarm Services

## Quick Start

### 1. In Your FastAPI Service (e.g., `services/farms/main.py`)

```python
from fastapi import FastAPI
from services.shared.logging_config import setup_logging

app = FastAPI()
logger = setup_logging("ecofarm-farms")

@app.on_event("startup")
async def startup():
    logger.info("Farms service starting up")

@app.get("/health")
async def health():
    logger.info("Health check called")
    return {"status": "ok"}

@app.get("/farms")
async def get_farms():
    try:
        logger.info("Fetching farms from database")
        # Your code here
        return {"farms": []}
    except Exception as e:
        logger.error(f"Failed to fetch farms: {e}")
        raise
```

### 2. Set Environment Variables (in Render)

For **Axiom** (current):
```
LOGGING_BACKEND=axiom
AXIOM_API_TOKEN=xaat_...
AXIOM_DATASET=ecofarm
SENTRY_ENV=production
SERVICE_NAME=ecofarm-farms
```

For **Loki** (future - when you self-host):
```
LOGGING_BACKEND=loki
LOKI_URL=http://your-loki-server:3100
SENTRY_ENV=production
SERVICE_NAME=ecofarm-farms
```

### 3. View Logs in Axiom

1. Go to https://axiom.co dashboard
2. Click your **ecofarm** dataset
3. See real-time logs streaming in

---

## Switching to Loki Later

When you're ready to self-host Loki:

1. Deploy Loki (e.g., on separate VPS)
2. In Render service env vars, change:
   ```
   LOGGING_BACKEND=loki
   LOKI_URL=https://your-loki-server:3100
   ```
3. Done! No code changes needed.

---

## How It Works

- **Console logs** always print (for Render dashboard)
- **Axiom logs** send to Axiom API (current)
- **Loki logs** send to Loki HTTP API (future)
- If logging backend fails, app keeps running (graceful degradation)

---

## Available Log Levels

```python
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

Each log includes:
- Timestamp
- Service name
- Environment (prod/staging)
- Function name
- Line number
- Full message
