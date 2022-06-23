import struct
from sqlalchemy.orm import Session
import models
import schemas


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
            data = struct.unpack("20f1s", byte_data)
            payloads.append(schemas.PayloadIdentified(
                linux_epoch=data[0],
                wind_angle=data[1],
                wind_speed=data[2],
                air_pressure=data[3],
                air_temperature=data[4],
                solar_panel_voltage=data[5],
                solar_panel_power=data[6],
                heading=data[7],
                gps_lat=data[8],
                gps_lon=data[9],
                water_temp=data[10],
                roll=data[11],
                pitch=data[12],
                battery_current=data[13],
                battery_voltage=data[14],
                cpu_average_usage=data[15],
                memory_usage=data[16],
                available_disk_space=data[17],
                left_motor_pwm=data[18],
                right_motor_pwm=data[19],
                mission_status=data[20],
                iridium_latitude=parsed_message.iridium_latitude,
                iridium_longitude=parsed_message.iridium_longitude,
                transmit_time_utc=parsed_message.transmit_time,
            ))
    except Exception as error:
        print(error)
    return payloads

