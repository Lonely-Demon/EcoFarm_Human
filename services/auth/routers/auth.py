from fastapi import APIRouter, Depends, HTTPException, status
from services.auth import schemas, crud
from common.db import get_db
from sqlalchemy.orm import Session
from supabase import create_client
from common.config import settings

router = APIRouter()

supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

@router.post('/register', response_model=schemas.UserResponse)
def register_user(payload: schemas.RegisterUser, db: Session = Depends(get_db)):
    # Create user in Supabase Auth
    try:
        auth_resp = supabase_client.auth.sign_up({
            'email': payload.email,
            'password': payload.password
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    # Supabase may return user object
    user_obj = auth_resp.user if hasattr(auth_resp, 'user') else auth_resp
    supabase_id = user_obj['id'] if isinstance(user_obj, dict) else user_obj.id

    # Create user in our DB
    db_user = crud.get_user_by_email(db, payload.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')

    db_user = crud.create_user(db, payload, supabase_id)
    return db_user

@router.post('/login')
def login_user(payload: schemas.LoginUser):
    # Proxy login to Supabase
    try:
        auth_resp = supabase_client.auth.sign_in_with_password({
            'email': payload.email,
            'password': payload.password
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if not auth_resp or auth_resp['data'] is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    return auth_resp
