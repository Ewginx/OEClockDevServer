from pydantic import BaseModel
from sqlalchemy.orm import Session
from loguru import logger
from . import models, schemas


def create(db=Session, settings_scheme=BaseModel):
    setting_db = models.Settings(**settings_scheme.model_dump())
    db.add(setting_db)
    db.commit()
    db.refresh(setting_db)

def model_is_empty(db):
    return False if db.query(models.Settings).first() else True

def get_filled_schema():
    return schemas.SettingsSchema(
        ssid="your_ssid",
        password="password1234",
        ip_address="127.0.0.1",
        gateway="127.0.0.1",
        sta_login="admin",
        sta_password="admin1234",
        auto_brightness=True,
        auto_theme_change=True,
        threshold=120,
        brightness_level=128,
        timezone_posix="EST",
        digital_main_screen=True,
        weather_enabled=True,
        api_key="cQrfF12#jfdsJFSUcz-AX13",
        city="London",
        language="en",
        request_period=3,
        dark_theme_enabled=True,
        light_background_color="#313d341",
        light_second_color="#97d34e",
        dark_background_color="#effd34e",
        dark_second_color="#32d34e",
    )


def prepopulate_db(db=Session):
    db = next(db)
    if model_is_empty(db):
        create(db, get_filled_schema())
        logger.info("Settings table was prepopulated")
