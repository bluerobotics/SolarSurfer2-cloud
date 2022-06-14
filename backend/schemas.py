from pydantic import BaseModel


class RockblockMessageBase(BaseModel):
    imei: int
    serial: int
    momsn: int
    transmit_time: str
    iridium_latitude: float
    iridium_longitude: float
    iridium_cep: int
    data: str

class RockblockMessageRegistered(RockblockMessageBase):
    id: int

    class Config:
        orm_mode = True

default_rockblock_message = RockblockMessageBase(**{
    "imei": -1,
    "serial": -1,
    "momsn": -1,
    "transmit_time": "00-00-00 00:00:00",
    "iridium_latitude": 0.0000,
    "iridium_longitude": 0.0000,
    "iridium_cep": -1,
    "data": "aaaa0000",
})