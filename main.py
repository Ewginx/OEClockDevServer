from fastapi import FastAPI, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from loguru import logger

app = FastAPI()


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


@app.post("/set_time", status_code=status.HTTP_202_ACCEPTED)
async def set_time(request: Request):
    time_json = await request.json()
    posix_time = int(time_json["time"]) / 1000
    date = datetime.utcfromtimestamp(posix_time).strftime("%Y-%m-%dT%H:%M:%S")
    logger.info(f"Get post about date: {date}")
    return None


@app.post("/setup_time", status_code=status.HTTP_202_ACCEPTED)
async def setup_time(request: Request):
    time_json = await request.json()
    timezone = time_json["timezone"]
    digital_clock = time_json["digital_clock"]
    logger.info(
        f"Time settings recieved: TZ={timezone}, main screen is {"DigitalClock" if digital_clock else "AnalogClock"}"
    )
    return None


@app.get("/get_data", status_code=status.HTTP_200_OK)
async def get_data():
    data = jsonable_encoder({"password": 1234})
    return JSONResponse(content=data)


app.mount("/", StaticFiles(directory="static", html=True), name="static")
