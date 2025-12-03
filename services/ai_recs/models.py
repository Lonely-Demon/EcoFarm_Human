from sqlalchemy import Column, JSON, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from common.db import Base

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True)
    farm_id = Column(UUID(as_uuid=True), nullable=True)
    sector_id = Column(UUID(as_uuid=True), nullable=True)
    inputs = Column(JSON, nullable=False)
    results = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
