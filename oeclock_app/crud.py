from pydantic import BaseModel
from sqlalchemy.orm import Session
from loguru import logger
from . import models, schemas
from .database import Base


def get_data(db: Session):
    return None


def update_or_create(db: Session, settings_scheme: BaseModel, model: Base):
    if not (setting_db := db.query(model).first()):
        setting_db = model(**settings_scheme.model_dump())
        db.add(setting_db)
        db.commit()
        db.refresh(setting_db)
        return setting_db
    db.query(model).filter_by(id=setting_db.id).update(settings_scheme.model_dump())
    db.commit()
    db.refresh(setting_db)
    return setting_db


def update_or_create_wifi_settings(db: Session, wifi_settings: schemas.WifiSchema):
    return update_or_create(db, wifi_settings, models.WifiSettings)


def update_or_create_brightness_settings(
    db: Session, brightness_settings: schemas.BrightnessSchema
):
    return update_or_create(db, brightness_settings, models.BrightnessSettings)


def update_or_create_time_settings(db: Session, time_settings: schemas.TimeSchema):
    return update_or_create(db, time_settings, models.TimeSettings)


def update_or_create_weather_settings(
    db: Session, weather_settings: schemas.WeatherSchema
) -> models.WeatherSettings:
    return update_or_create(db, weather_settings, models.WeatherSettings)


def update_or_create_theme_settings(
    db: Session, theme_settings: schemas.ThemeSchema
) -> models.ThemeSettings:
    return update_or_create(db, theme_settings, models.ThemeSettings)
