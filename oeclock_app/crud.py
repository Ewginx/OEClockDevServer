from pydantic import BaseModel
from sqlalchemy.orm import Session
from loguru import logger
from . import models


def get_settings_from_db_as_dict(db: Session):
    if setting_db := db.query(models.Settings).first():
        setting_db_dict = setting_db.as_dict()
        return setting_db_dict
    else:
        return {}


def update_settings_model(db: Session, settings_scheme: BaseModel):
    setting_db = db.query(models.Settings).first()
    db.query(models.Settings).filter_by(id=setting_db.id).update(
        settings_scheme.model_dump()
    )
    db.commit()
    db.refresh(setting_db)
    return setting_db
