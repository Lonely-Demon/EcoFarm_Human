from fastapi import APIRouter, Depends, HTTPException, status
from services.farms import schemas, crud
from common.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/', response_model=schemas.FarmResponse)
def create_farm(payload: schemas.FarmCreate, db: Session = Depends(get_db), x_user_id: str = "test-user"):
    # x_user_id simulates authenticated user's supabase id for now.
    try:
        f = crud.create_farm(db, x_user_id, payload)
        return f
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/{farm_id}', response_model=schemas.FarmResponse)
def get_farm(farm_id: str, db: Session = Depends(get_db)):
    f = crud.get_farm(db, farm_id)
    if not f:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Farm not found')
    return f

@router.post('/{farm_id}/sectors', response_model=schemas.SectorResponse)
def add_sector(farm_id: str, payload: schemas.SectorCreate, db: Session = Depends(get_db)):
    try:
        s = crud.create_sector(db, farm_id, payload)
        return s
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
