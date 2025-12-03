from sqlalchemy.orm import Session
from services.auth import models
from services.auth.schemas import RegisterUser
from uuid import uuid4


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: RegisterUser, supabase_id: str):
    u = models.User(
        id=uuid4(),
        supabase_id=supabase_id,
        email=user.email,
        name=user.name,
        phone=user.phone,
        language=user.language,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u
