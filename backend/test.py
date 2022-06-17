from datetime import datetime
from random import randint, uniform
import struct
from faker import Faker
from pprint import pprint
import requests
from schemas import RockblockMessageBase


ROCKBLOCK_WEBHOOK_ROUTE = "http://127.0.0.1:8000/rockblock-messages"
# ROCKBLOCK_WEBHOOK_ROUTE = "http://143.198.58.63:8000/rockblock-messages"

fake = Faker()

message = RockblockMessageBase(**{
    "imei": 300234010753370,
    "serial": 12345,
    "momsn": 12345,
    "transmit_time": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
    "iridium_latitude": fake.coordinate(),
    "iridium_longitude": fake.coordinate(),
    "iridium_cep": randint(1, 10),
    "data": struct.pack("7f", uniform(0, 9), uniform(0, 9), uniform(0, 9), uniform(0, 9), uniform(0, 9), uniform(0, 9), uniform(0, 9)).hex(),
})
print(">")
pprint(message.dict())
requests.post(ROCKBLOCK_WEBHOOK_ROUTE, message.json())
