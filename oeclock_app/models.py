from sqlalchemy import Boolean, Column, Integer, String
from .database import Base


class WifiSettings(Base):
    __tablename__ = "wifi_settings"

    id = Column(Integer, primary_key=True, index=True)
    ssid = Column(String, unique=True, index=True)
    password = Column(String)
    ip_address = Column(String)
    gateway = Column(String)
    sta_login = Column(String)
    sta_password = Column(String)


class BrightnessSettings(Base):
    __tablename__ = "brightness_settings"

    id = Column(Integer, primary_key=True, index=True)
    auto_brightness = Column(Boolean)
    auto_theme_change = Column(Boolean)
    threshold = Column(Integer)
    brightness_level = Column(Integer)


class TimeSettings(Base):
    __tablename__ = "time_settings"

    id = Column(Integer, primary_key=True, index=True)
    timezone_posix = Column(String)
    digital_main_screen = Column(Boolean, default=True)


class WeatherSettings(Base):
    __tablename__ = "weather_settings"

    id = Column(Integer, primary_key=True, index=True)
    weather_enabled = Column(Boolean)
    api_key = Column(String)
    city = Column(String)
    language = Column(String)
    request_period = Column(Integer)


class ThemeSettings(Base):
    __tablename__ = "theme_settings"

    id = Column(Integer, primary_key=True, index=True)
    dark_theme_enabled = Column(Boolean)
    light_background_color = Column(String)
    light_second_color = Column(String)
    dark_background_color = Column(String)
    dark_second_color = Column(String)
