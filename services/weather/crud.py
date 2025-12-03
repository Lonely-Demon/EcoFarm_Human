from sqlalchemy.orm import Session
from services.weather import models
from sqlalchemy import select
from uuid import uuid4
import hashlib
import json
from datetime import datetime, timedelta

CACHE_TTL_MINUTES = 60


def location_hash(lat: float, lon: float):
    key = f"{lat:.6f}:{lon:.6f}"
    return hashlib.sha256(key.encode('utf-8')).hexdigest()


def get_cached_weather(db: Session, lat: float, lon: float):
    h = location_hash(lat, lon)
    stmt = select(models.WeatherCache).where(models.WeatherCache.location_hash == h)
    res = db.execute(stmt).scalars().first()
    if not res:
        return None

    now = datetime.utcnow()
    if res.cached_at + timedelta(minutes=CACHE_TTL_MINUTES) < now:
        return None
    return res


def save_weather_cache(db: Session, provider: str, lat: float, lon: float, payload: dict):
    h = location_hash(lat, lon)
    existing = db.query(models.WeatherCache).filter(models.WeatherCache.location_hash == h).first()
    if existing:
        existing.provider = provider
        existing.payload = payload
        existing.cached_at = datetime.utcnow()
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    w = models.WeatherCache(id=uuid4(), provider=provider, location_hash=h, lat=lat, lon=lon, payload=payload)
    db.add(w)
    db.commit()
    db.refresh(w)
    return w
