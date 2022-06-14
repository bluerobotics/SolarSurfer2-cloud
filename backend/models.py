from sqlalchemy import Boolean, Column, Integer, String, Float

from database import Base


class RockblockMessage(Base):
    __tablename__ = "rockblock_mesages"

    id = Column(Integer, primary_key=True, index=True)
    imei = Column(Integer)
    serial = Column(Integer)
    momsn = Column(Integer)
    transmit_time = Column(String)
    iridium_latitude = Column(Float)
    iridium_longitude = Column(Float)
    iridium_cep = Column(Integer)
    data = Column(String)
