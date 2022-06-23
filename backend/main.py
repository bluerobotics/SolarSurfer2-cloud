#! /usr/bin/env python3

import uvicorn
import json
from pprint import pprint
from typing import Any, List
from fastapi import Depends, FastAPI, Request
from starlette.responses import Response as StarletteResponse
from schemas import RockblockMessageBase, default_rockblock_message, RockblockMessageRegistered, PayloadIdentified
from crud import create_rockblock_message, get_last_rockblock_message, get_rockblock_messages, get_payloads
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine

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

@app.get("/")
async def root():
    return {"message": "Hello from the Solar Surfer 2 API!"}

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
