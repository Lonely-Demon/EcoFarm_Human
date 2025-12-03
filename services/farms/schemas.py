from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID

class GeoJSONGeometry(BaseModel):
    type: str
    coordinates: Any

class FarmCreate(BaseModel):
    name: str
    geom: GeoJSONGeometry

class FarmResponse(BaseModel):
    id: UUID
    name: str
    area_ha: Optional[float]
    geom: Optional[GeoJSONGeometry]

    class Config:
        orm_mode = True

class SectorCreate(BaseModel):
    name: Optional[str] = None
    geom: GeoJSONGeometry

class SectorResponse(BaseModel):
    id: UUID
    name: Optional[str] = None
    geom: Optional[GeoJSONGeometry]

    class Config:
        orm_mode = True
