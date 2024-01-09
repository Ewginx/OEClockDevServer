import asyncio
import random
from datetime import datetime
from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from loguru import logger
from sqlalchemy.orm import Session

from oeclock_app import crud, models, schemas
from oeclock_app.database import SessionLocal, engine
from oeclock_app.prepopulate_db import prepopulate_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBasic()


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
@app.get("/alarm_clock", status_code=status.HTTP_301_MOVED_PERMANENTLY)
def redirect():
    return RedirectResponse("/")


@app.get("/")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username == "admin" and credentials.password == "admin1234":
        return FileResponse("static/index.html")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect login or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.get("/logout")
def logout():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Logged out",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.put("/time", status_code=status.HTTP_202_ACCEPTED)
async def set_time(time: schemas.SetTimeSchema):
    date = datetime.utcfromtimestamp(time.time).strftime("%Y-%m-%dT%H:%M:%S")
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


@app.put("/settings/alarm_clock", status_code=status.HTTP_200_OK)
async def save_alarm_clock_settings(
    wifi_settings: schemas.AlarmClockSchema, db: Session = Depends(get_db)
):
    if updated_settings := crud.update_settings_model(db=db, settings_scheme=wifi_settings):
        logger.info(f"Alarm settings updated! New values are {updated_settings.weekdays_time}")


class MyStatics(StaticFiles):
    def is_not_modified(self, response_headers, request_headers) -> bool:
        return False


@app.get("/settings", status_code=status.HTTP_200_OK, response_model=schemas.SettingsSchema)
async def get_settings(db: Session = Depends(get_db)):
    serialized_settings = schemas.SettingsSchema(**crud.get_settings_from_db_as_dict(db))
    return JSONResponse(content=serialized_settings.model_dump_json())


@app.post("/ota_update", status_code=status.HTTP_200_OK)
async def load_fw(file: UploadFile):
    logger.info(file.filename)
    json_content = {}
    if ".bin" in file.filename:
        json_content = {"update": True}
    else:
        json_content = {"update": False}
    return JSONResponse(content=jsonable_encoder(json_content))


app.mount("/", MyStatics(directory="static", html=True), name="static")
