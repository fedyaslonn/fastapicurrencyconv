from sqlalchemy.orm import Session
from . import models, schemas


def get_last_operation(db: Session):
    last_operation = db.query(models.Operation).order_by(models.Operation.created_at.desc()).first()
    return last_operation

def get_operations(db: Session):
    return db.query(models.Operation).all()
