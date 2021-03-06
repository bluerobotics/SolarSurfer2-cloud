#! /usr/bin/env python3

import uvicorn
import json
from pprint import pprint
from typing import Any, List
from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response as StarletteResponse
from schemas import RockblockMessageBase, default_rockblock_message, RockblockMessageRegistered, PayloadIdentified
from crud import create_rockblock_message, get_last_rockblock_message, get_rockblock_messages, get_payloads
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from SolarSurfer2.services.sats_comm.messages import deserialize
from weather import get_weather_data

models.Base.metadata.create_all(bind=engine)

class PrettyJSONResponse(StarletteResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(", ", ": "),
        ).encode(self.charset)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

last_rockblock_message = default_rockblock_message


app = FastAPI(
    title="Solar Surfer 2 API",
    description="This thing is going to Hawaii, one way or another.",
    default_response_class=PrettyJSONResponse,
)

app.mount("/ui", StaticFiles(directory="../frontend", html = True), name="static")

@app.post("/rockblock-messages")
async def rockblock_web_hook_post_route(request: Request, db: Session = Depends(get_db)):
    raw_message = await request.body()
    print('raw', raw_message)
    message = RockblockMessageBase(**json.loads(raw_message))
    print('message', message)
    create_rockblock_message(db, message)
    pprint(message.dict())
    return message

@app.get("/rockblock-message", response_model=RockblockMessageRegistered)
async def last_rockblock_message_route(db: Session = Depends(get_db)) -> Any:
    return get_last_rockblock_message(db)

@app.get("/rockblock-messages", response_model=List[RockblockMessageRegistered])
async def rockblock_messages_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> Any:
    return get_rockblock_messages(db, skip, limit)

@app.get("/payloads", response_model=List[PayloadIdentified])
async def payloads_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> Any:
    return get_payloads(db, skip, limit)

@app.get("/weather")
async def weather(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> Any:
    last = get_last_rockblock_message(db)
    parsed_message = deserialize(bytes.fromhex(last.data.decode()))
    lat, lon = parsed_message["lattitude"], parsed_message["longitude"]
    return get_weather_data(lat, lon)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
