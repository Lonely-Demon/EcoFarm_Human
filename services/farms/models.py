from sqlalchemy import Column, String, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from common.db import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=True)
    area_ha = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Sector(Base):
    __tablename__ = "sectors"

    id = Column(UUID(as_uuid=True), primary_key=True)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id"), nullable=False)
    name = Column(String, nullable=True)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=True)
    crop = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
