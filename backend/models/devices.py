"""
This file is useful to abstract database implementation
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from core.database import get_db

Base = declarative_base()


class Device(Base):
    """
    Class to interact with a device inside the database.
    """

    __tablename__ = 'devices'
    hostname = Column(String, primary_key=True)
    mac = Column(String)
    interface = Column(String)


    @classmethod
    def get_devices(cls):
        """
        Get all devices
        """
        devices = None
        db = get_db()
        try:
            devices = db.query(Device).all()
        finally:
            db.close()
            return devices
