from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from common.db import Base

class WeatherCache(Base):
    __tablename__ = "weather_cache"

    id = Column(UUID(as_uuid=True), primary_key=True)
    provider = Column(String, nullable=False)
    location_hash = Column(String, nullable=False, index=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    payload = Column(JSON, nullable=False)
    cached_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
