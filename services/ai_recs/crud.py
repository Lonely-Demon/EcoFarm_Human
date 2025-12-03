from sqlalchemy.orm import Session
from services.ai_recs import models
from uuid import uuid4


def save_recommendation(db: Session, inputs: dict, results: dict):
    r = models.AIRecommendation(id=uuid4(), inputs=inputs, results=results)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r
