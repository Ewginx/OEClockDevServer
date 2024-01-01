from sqlalchemy import Boolean, Column, Integer, String
from .database import Base


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)

    ssid = Column(String, unique=True, index=True)
    password = Column(String)
    ip_address = Column(String)
    gateway = Column(String)
    sta_login = Column(String)
    sta_password = Column(String)

    auto_brightness = Column(Boolean)
    auto_theme_change = Column(Boolean)
    threshold = Column(Integer)
    brightness_level = Column(Integer)

    timezone_posix = Column(String)
    digital_main_screen = Column(Boolean, default=True)

    weather_enabled = Column(Boolean)
    api_key = Column(String)
    city = Column(String)
    language = Column(String)
    request_period = Column(Integer)

    dark_theme_enabled = Column(Boolean)
    light_background_color = Column(String)
    light_second_color = Column(String)
    dark_background_color = Column(String)
    dark_second_color = Column(String)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}