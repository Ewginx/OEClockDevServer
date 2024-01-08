from loguru import logger
from pydantic import BaseModel
from sqlalchemy.orm import Session

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
        ap_login="admin",
        ap_password="admin1234",
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
        light_primary_color=1234455,
        light_second_color=1234455,
        light_screen_color=1234455,
        light_card_color=1234455,
        light_text_color=1234455,
        light_grey_color=1234455,
        dark_primary_color=1234455,
        dark_second_color=123445,
        dark_screen_color=123445,
        dark_card_color=123445,
        dark_text_color=123445,
        dark_grey_color=123445,
        weekdays_time="18:30",
        weekdays_enabled=True,
        weekends_time="18:30",
        weekends_enabled=True,
        one_off_time="18:30",
        one_off_enabled=True,
    )


def prepopulate_db(db=Session):
    db = next(db)
    if model_is_empty(db):
        create(db, get_filled_schema())
        logger.info("Settings table was prepopulated")
