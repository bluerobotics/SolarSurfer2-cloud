from pydantic import BaseModel


class RockblockMessageBase(BaseModel):
    imei: int
    serial: int
    momsn: int
    transmit_time: str
    iridium_latitude: float
    iridium_longitude: float
    iridium_cep: int
    data: bytes

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

class Payload(BaseModel):
    linux_epoch: float
    time_boot_ms: float
    time_unix_usec: float
    air_pressure: float
    air_temperature: float
    solar_panel_voltage: float
    solar_panel_power: float
    heading: float
    gps_lat: float
    gps_lon: float
    water_temp: float
    roll: float
    pitch: float
    battery_current: float
    battery_voltage: float
    cpu_average_usage: float
    memory_usage: float
    available_disk_space: float
    left_motor_pwm: float
    right_motor_pwm: float
    mission_status: str

class PayloadIdentified(Payload):
    iridium_latitude: float
    iridium_longitude: float
    transmit_time_utc: str