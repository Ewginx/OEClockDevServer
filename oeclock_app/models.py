from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)  # noqa

    ssid = Column(String, unique=True, index=True)
    password = Column(String)
    ip_address = Column(String)
    gateway = Column(String)
    ap_login = Column(String)
    ap_password = Column(String)

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
    light_primary_color = Column(Integer)
    light_second_color = Column(Integer)
    light_screen_color = Column(Integer)
    light_card_color = Column(Integer)
    light_text_color = Column(Integer)
    light_grey_color = Column(Integer)

    dark_primary_color = Column(Integer)
    dark_second_color = Column(Integer)
    dark_screen_color = Column(Integer)
    dark_card_color = Column(Integer)
    dark_text_color = Column(Integer)
    dark_grey_color = Column(Integer)

    weekdays_time = Column(String)
    weekdays_enabled = Column(Boolean)
    weekends_time = Column(String)
    weekends_enabled = Column(Boolean)
    one_off_time = Column(String)
    one_off_enabled = Column(Boolean)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
