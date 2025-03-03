from models.devices import Device as DeviceModel

from pydantic import BaseModel


class Device(BaseModel):
    hostname: str
    mac: str
    interface: str


    @classmethod
    def get_devices(cls):
        """
        Get all devices.
        """
        devices = DeviceModel.get_devices()
        return devices
