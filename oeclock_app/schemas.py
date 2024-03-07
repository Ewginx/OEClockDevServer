from pydantic import BaseModel


class WifiSchema(BaseModel):
    ssid: str
    password: str
    ip_address: str
    gateway: str
    ap_login: str
    ap_password: str


class BrightnessSchema(BaseModel):
    auto_brightness: bool
    auto_theme_change: bool
    threshold: int
    brightness_level: int


class TimeSchema(BaseModel):
    timezone_posix: str
    digital_main_screen: bool


class AlarmClockSchema(BaseModel):
    weekdays_time: str
    weekends_time: str
    one_off_time: str
    weekdays_enabled: bool
    weekends_enabled: bool
    one_off_enabled: bool


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

    light_primary_color: int
    light_second_color: int
    light_screen_color: int
    light_card_color: int
    light_text_color: int
    light_grey_color: int

    dark_primary_color: int
    dark_second_color: int
    dark_screen_color: int
    dark_card_color: int
    dark_text_color: int
    dark_grey_color: int


class RGBSchema(BaseModel):
    rgb_enabled: bool
    rgb_mode: int
    first_rgb_color: int
    second_rgb_color: int
    third_rgb_color: int
    rgb_delay: int
    rgb_brightness: int
    rgb_night: bool


class SettingsSchema(BaseModel):
    ssid: str
    password: str
    ip_address: str
    gateway: str
    ap_login: str
    ap_password: str
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
    light_primary_color: int
    light_second_color: int
    light_screen_color: int
    light_card_color: int
    light_text_color: int
    light_grey_color: int
    dark_primary_color: int
    dark_second_color: int
    dark_screen_color: int
    dark_card_color: int
    dark_text_color: int
    dark_grey_color: int

    weekdays_time: str
    weekdays_enabled: bool
    weekends_time: str
    weekends_enabled: bool
    one_off_time: str
    one_off_enabled: bool

    fs_space: int

    rgb_enabled: bool
    rgb_mode: int
    first_rgb_color: int
    second_rgb_color: int
    third_rgb_color: int
    rgb_delay: int
    rgb_brightness: int
    rgb_night: bool


class WebsocketSchema(BaseModel):
    temperature: float
    humidity: int
    lx: int
    battery_level: int
    max_free_block: int
    free_heap: int
    used_space: int
