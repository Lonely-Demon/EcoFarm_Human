"""
Centralized logging configuration for EcoFarm services.

Supports multiple backends:
- Axiom (current - log streaming)
- Loki (future - self-hosted option)

To switch backends, update LOGGING_BACKEND env var.
"""

import os
import json
import logging
from typing import Dict, Any
from datetime import datetime

# Configuration
LOGGING_BACKEND = os.getenv("LOGGING_BACKEND", "axiom")  # axiom or loki
AXIOM_API_TOKEN = os.getenv("AXIOM_API_TOKEN", "")
AXIOM_DATASET = os.getenv("AXIOM_DATASET", "ecofarm")
LOKI_URL = os.getenv("LOKI_URL", "http://localhost:3100")  # For future Loki
SERVICE_NAME = os.getenv("SERVICE_NAME", "ecofarm-service")
ENVIRONMENT = os.getenv("SENTRY_ENV", "production")


class AxiomHandler(logging.Handler):
    """Send logs to Axiom via HTTP."""
    
    def __init__(self, api_token: str, dataset: str):
        super().__init__()
        self.api_token = api_token
        self.dataset = dataset
        self.endpoint = f"https://api.axiom.co/v1/datasets/{dataset}/ingest"
    
    def emit(self, record: logging.LogRecord):
        """Send log record to Axiom."""
        try:
            import requests
            
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "service": SERVICE_NAME,
                "environment": ENVIRONMENT,
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }
            
            # Add exception info if present
            if record.exc_info:
                log_entry["exception"] = self.format(record)
            
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            }
            
            requests.post(
                self.endpoint,
                json=[log_entry],
                headers=headers,
                timeout=5,
            )
        except Exception as e:
            # Silently fail - don't crash app if logging fails
            print(f"Failed to send log to Axiom: {e}")


class LokiHandler(logging.Handler):
    """Send logs to Loki via HTTP (for future use)."""
    
    def __init__(self, loki_url: str):
        super().__init__()
        self.loki_url = loki_url
        self.endpoint = f"{loki_url}/loki/api/v1/push"
    
    def emit(self, record: logging.LogRecord):
        """Send log record to Loki."""
        try:
            import requests
            
            log_line = json.dumps({
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "service": SERVICE_NAME,
                "module": record.module,
                "function": record.funcName,
            })
            
            payload = {
                "streams": [
                    {
                        "stream": {
                            "job": SERVICE_NAME,
                            "env": ENVIRONMENT,
                            "level": record.levelname.lower(),
                        },
                        "values": [
                            [str(int(datetime.utcnow().timestamp() * 1e9)), log_line]
                        ],
                    }
                ]
            }
            
            requests.post(self.endpoint, json=payload, timeout=5)
        except Exception as e:
            print(f"Failed to send log to Loki: {e}")


def setup_logging(service_name: str = "ecofarm-service") -> logging.Logger:
    """
    Configure logging based on LOGGING_BACKEND env var.
    
    Usage in your FastAPI app:
        logger = setup_logging("ecofarm-farms")
        logger.info("Service started")
    """
    global SERVICE_NAME
    SERVICE_NAME = service_name
    
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Console handler (always)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Backend-specific handler
    if LOGGING_BACKEND == "axiom" and AXIOM_API_TOKEN:
        try:
            axiom_handler = AxiomHandler(AXIOM_API_TOKEN, AXIOM_DATASET)
            logger.addHandler(axiom_handler)
            logger.info(f"Axiom logging initialized (dataset: {AXIOM_DATASET})")
        except Exception as e:
            logger.warning(f"Failed to initialize Axiom handler: {e}")
    
    elif LOGGING_BACKEND == "loki":
        try:
            loki_handler = LokiHandler(LOKI_URL)
            logger.addHandler(loki_handler)
            logger.info(f"Loki logging initialized (url: {LOKI_URL})")
        except Exception as e:
            logger.warning(f"Failed to initialize Loki handler: {e}")
    
    else:
        logger.warning(
            f"Unknown logging backend: {LOGGING_BACKEND}. "
            "Logs will only go to console."
        )
    
    return logger
