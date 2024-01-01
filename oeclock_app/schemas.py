from pydantic import BaseModel


class WifiSchema(BaseModel):
    ssid: str
    password: str
    ip_address: str
    gateway: str
    sta_login: str
    sta_password: str


class BrightnessSchema(BaseModel):
    auto_brightness: bool
    auto_theme_change: bool
    threshold: int
    brightness_level: int


class TimeSchema(BaseModel):
    timezone_posix: str
    digital_main_screen: bool


class SetTimeSchema(BaseModel):
    time: int


class WeatherSchema(BaseModel):
    weather_enabled: bool
    api_key: str
    city: str
    language: str
    request_period: int


class ThemeSchema(BaseModel):
    dark_theme_enabled: bool
    light_background_color: str
    light_second_color: str
    dark_background_color: str
    dark_second_color: str

class SettingsSchema(BaseModel):
    ssid: str
    password: str
    ip_address: str
    gateway: str
    sta_login: str
    sta_password: str
    auto_brightness: bool
    auto_theme_change: bool
    threshold: int
    brightness_level: int
    timezone_posix: str
    digital_main_screen: bool
    weather_enabled: bool
    api_key: str
    city: str
    language: str
    request_period: int
    dark_theme_enabled: bool
    light_background_color: str
    light_second_color: str
    dark_background_color: str
    dark_second_color: str
