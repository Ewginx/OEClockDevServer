import asyncio
import random
from datetime import datetime

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .prepopulate_db import prepopulate_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


prepopulate_db(get_db())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            websocket_schema = schemas.WebsocketSchema(
                temperature=random.uniform(23, 25),
                humidity=random.randint(40, 67),
                lx=random.randint(0, 250),
                battery_level=random.randint(15, 100),
            )
            await websocket.send_text(websocket_schema.model_dump_json())
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        logger.info("Client disconnected")


@app.get("/debug", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/ota", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/sounds", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/rgb", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/weather", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/theme", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/wifi", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/brightness", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@app.get("/time", status_code=status.HTTP_301_MOVED_PERMANENTLY)
def redirect():
    return RedirectResponse("/")


@app.put("/time", status_code=status.HTTP_202_ACCEPTED)
async def set_time(time: schemas.SetTimeSchema):
    date = datetime.utcfromtimestamp(time.time / 1000).strftime("%Y-%m-%dT%H:%M:%S")
    logger.info(f"Get put request, converted date is (UTC): {date}")
    return None


@app.put("/settings/time", status_code=status.HTTP_200_OK)
async def save_time_settings(time_settings: schemas.TimeSchema, db: Session = Depends(get_db)):
    if updated_settings := crud.update_settings_model(db=db, settings_scheme=time_settings):
        logger.info(f"Time settings updated! New values are {updated_settings.timezone_posix}")
    return None


@app.put("/settings/weather", status_code=status.HTTP_200_OK)
async def save_weather_settings(
    weather_settings: schemas.WeatherSchema, db: Session = Depends(get_db)
):
    if updated_settings := crud.update_settings_model(db=db, settings_scheme=weather_settings):
        logger.info(f"Weather settings updated! New values are {updated_settings.language}")
    return None


@app.put("/settings/theme", status_code=status.HTTP_200_OK)
async def save_theme_settings(theme_settings: schemas.ThemeSchema, db: Session = Depends(get_db)):
    if updated_settings := crud.update_settings_model(db=db, settings_scheme=theme_settings):
        logger.info(f"Theme settings updated! New values are {updated_settings.dark_theme_enabled}")
    return None


@app.put("/settings/brightness", status_code=status.HTTP_200_OK)
async def save_brightness_settings(
    brightness_settings: schemas.BrightnessSchema, db: Session = Depends(get_db)
):
    if updated_settings := crud.update_settings_model(db=db, settings_scheme=brightness_settings):
        logger.info(
            f"Brightness settings updated! New values are {updated_settings.auto_brightness}"
        )
    return None


@app.put("/settings/wifi", status_code=status.HTTP_200_OK)
async def save_wifi_settings(wifi_settings: schemas.WifiSchema, db: Session = Depends(get_db)):
    if updated_settings := crud.update_settings_model(db=db, settings_scheme=wifi_settings):
        logger.info(f"WiFi settings updated! New values are {updated_settings.ip_address}")


class MyStatics(StaticFiles):
    def is_not_modified(self, response_headers, request_headers) -> bool:
        return False


@app.get("/settings", status_code=status.HTTP_200_OK, response_model=schemas.SettingsSchema)
async def get_settings(db: Session = Depends(get_db)):
    serialized_settings = schemas.SettingsSchema(**crud.get_settings_from_db_as_dict(db))
    return JSONResponse(content=serialized_settings.model_dump_json())


app.mount("/", MyStatics(directory="static", html=True), name="static")
