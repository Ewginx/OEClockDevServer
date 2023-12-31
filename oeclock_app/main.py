from fastapi import Depends, FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from loguru import logger
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/debug", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/ota", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/sounds", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/rgb", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/weather", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/theme", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/wifi", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/brightness", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/time", status_code=status.HTTP_301_MOVED_PERMANENTLY)
def time():
    return RedirectResponse("/")


@app.post("/time", status_code=status.HTTP_202_ACCEPTED)
async def set_time(time: schemas.SetTimeSchema):
    date = datetime.utcfromtimestamp(time.time / 1000).strftime("%Y-%m-%dT%H:%M:%S")
    logger.info(f"Get POST request, converted date is (UTC): {date}")
    return None


@app.post("/settings/time", status_code=status.HTTP_200_OK)
async def setup_time(time_settings: schemas.TimeSchema, db: Session = Depends(get_db)):
    if updated_time_settings:= crud.update_or_create_time_settings(db=db, time_settings=time_settings):
        logger.info(f"Time settings updated! New values are {updated_time_settings.timezone_posix} {updated_time_settings.main_screen}")
    return None

@app.post("/settings/weather", status_code=status.HTTP_200_OK)
async def setup_weather(weather_settings: schemas.WeatherSchema, db: Session = Depends(get_db)):
    if updated_weather_settings:= crud.update_or_create_weather_settings(db=db, weather_setting=weather_settings):
        logger.info(f"Weather settings updated! New values are {updated_weather_settings.language} {updated_weather_settings.city}")
    return None

@app.post("/settings/theme", status_code=status.HTTP_200_OK)
async def setup_theme(theme_settings: schemas.ThemeSchema, db: Session = Depends(get_db)):
    if updated_theme_settings:= crud.update_or_create_theme_settings(db=db, theme_settings=theme_settings):
        logger.info(f"Theme settings updated! New values are {updated_theme_settings.dark_theme_enabled} {updated_theme_settings.dark_background_color}")
    return None

@app.post("/settings/brightness", status_code=status.HTTP_200_OK)
async def setup_brightness(brightness_settings: schemas.BrightnessSchema, db: Session = Depends(get_db)):
    if updated_brightness_settings:= crud.update_or_create_brightness_settings(db=db, brightness_settings=brightness_settings):
        logger.info(f"Brightness settings updated! New values are {updated_brightness_settings.auto_brightness} {updated_brightness_settings.auto_theme_change}")
    return None

@app.post("/settings/wifi", status_code=status.HTTP_200_OK)
async def setup_wifi(wifi_settings: schemas.WifiSchema, db: Session = Depends(get_db)):
    if updated_wifi_settings:= crud.update_or_create_wifi_settings(db=db, wifi_settings=wifi_settings):
        logger.info(f"WiFi settings updated! New values are {updated_wifi_settings.ip_address} {updated_wifi_settings.ssid}")
    return None

@app.get("/settings", status_code=status.HTTP_200_OK)
async def get_data():
    data = jsonable_encoder({"password": 1234})
    return JSONResponse(content=data)


app.mount("/", StaticFiles(directory="static", html=True), name="static")
