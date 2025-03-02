from libs.devices import get_devices, status_checker
from core.config import get_config

from fastapi import APIRouter

devices = APIRouter(
    prefix="",
    tags=["devices"]
)

# Get config
config = get_config()

@devices.get("/devices")
def retrieve_devices():
    devices = get_devices()
    return {"devices": devices}
