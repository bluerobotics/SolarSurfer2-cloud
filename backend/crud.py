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