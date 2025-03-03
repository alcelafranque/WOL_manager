from core.config import get_config
from schemas.devices import Device

from fastapi import APIRouter


devices = APIRouter(
    prefix="",
    tags=["devices"]
)

# Get config
config = get_config()

@devices.get("/devices")
def retrieve_devices():
    devices = Device.get_devices()
    return {"devices": devices}

@devices.post("/status")
def get_status(device: Device):
    device = Device(**device.dict())
    status = device.check_status(config)
    return {"status": status}
