from sqlalchemy.orm import Session
from services.farms import models
from services.farms.schemas import FarmCreate, SectorCreate
from uuid import uuid4
from geoalchemy2.shape import from_shape
from shapely.geometry import shape


def create_farm(db: Session, user_id, farm: FarmCreate):
    # Convert GeoJSON to WKB geometry via shapely
    geojson = farm.geom.dict()
    geom_shape = shape(geojson)
    wkb = from_shape(geom_shape, srid=4326)

    f = models.Farm(
        id=uuid4(),
        user_id=user_id,
        name=farm.name,
        geom=wkb,
    )
    db.add(f)
    db.commit()
    db.refresh(f)
    return f


def get_farm(db: Session, farm_id: str):
    return db.query(models.Farm).filter(models.Farm.id == farm_id).first()


def create_sector(db: Session, farm_id, sector: SectorCreate):
    geojson = sector.geom.dict()
    geom_shape = shape(geojson)
    wkb = from_shape(geom_shape, srid=4326)
    s = models.Sector(id=uuid4(), farm_id=farm_id, name=sector.name, geom=wkb)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s
