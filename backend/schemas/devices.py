from models.devices import Device as DeviceModel

from pydantic import BaseModel, field_validator
from re import match
from wakeonlan import send_magic_packet


class Device(BaseModel):
    hostname: str
    mac: str
    interface: str

    @field_validator('mac')
    @classmethod
    def is_valid(cls, mac: str) -> bool:
        """
        Check if device fields are valid.
        :return: False if any field is invalid else True
        """
        # Check for valid mac
        mac_regex = r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}"
        if not match(mac_regex, mac):
            raise ValueError('"foobar" not found in a')

        return mac.lower()


    @classmethod
    def get_devices(cls) -> list[DeviceModel]:
        """
        Get all devices.
        """
        devices = DeviceModel.get_devices()

        return devices


    def start(self) -> None:
        """
        Send wake on lan packet to this device.
        Check if packets must be sent inside or outside the subnet.
        :param config: config of the project
        :return:
        """

        send_magic_packet(self.mac)


    def register(self) -> int:
        """
        Register new device
        :return: status code
        """

        devices = self.get_devices()

        # Check for duplicate
        for device in devices:
            if device.mac == self.mac:
                return 409

        DeviceModel.add_device(self.dict())
        return 200


    def delete(self) -> None:
        """
        Delete device
        :return: None
        """
        DeviceModel.delete_device(self.dict())
