import struct
from sqlalchemy.orm import Session
import models
import schemas

from SolarSurfer2.services.sats_comm.messages import deserialize


def create_rockblock_message(db: Session, message: schemas.RockblockMessageBase):
    db_message = models.RockblockMessage(
        imei=message.imei,
        serial=message.serial,
        momsn=message.momsn,
        transmit_time=message.transmit_time,
        iridium_latitude=message.iridium_latitude,
        iridium_longitude=message.iridium_longitude,
        iridium_cep=message.iridium_cep,
        data=message.data,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_last_rockblock_message(db: Session):
    return db.query(models.RockblockMessage).order_by(models.RockblockMessage.id.desc()).first()

def get_rockblock_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RockblockMessage).offset(skip).limit(limit).all()

def get_payloads(db: Session, skip: int = 0, limit: int = 100):
    messages = get_rockblock_messages(db, skip, limit)
    payloads = []
    try:
        for message in messages:
            parsed_message = schemas.RockblockMessageRegistered(**message.__dict__)
            hex_data = parsed_message.data
            byte_data = bytes.fromhex(hex_data.decode())
            print(len(byte_data))
            data = deserialize(byte_data)
            payloads.append(schemas.PayloadIdentified(
                linux_epoch=0,
                wind_angle=data['wind_angle'],
                wind_speed=data['wind_speed'],
                air_pressure=0,
                air_temperature=data['air_temperature'],
                solar_panel_voltage=data['solar_voltage'],
                solar_panel_power=data['solar_power'],
                heading=data['heading'],
                gps_lat=data['lattitude'],
                gps_lon=data['longitude'],
                water_temp=data['water_temperature'],
                roll=data['max_abs_roll'],
                pitch=data['max_abs_pitch'],
                battery_current=data['battery_current'],
                battery_voltage=data['battery_voltage'],
                cpu_average_usage=data['cpu'],
                memory_usage=data['memory'],
                available_disk_space=data['disk'],
                left_motor_pwm=data['throttle_first'],
                right_motor_pwm=data['throttle_second'],
                mission_status=0,
                iridium_latitude=parsed_message.iridium_latitude,
                iridium_longitude=parsed_message.iridium_longitude,
                transmit_time_utc=parsed_message.transmit_time,
            ))
    except Exception as error:
        print(error)
    return payloads

