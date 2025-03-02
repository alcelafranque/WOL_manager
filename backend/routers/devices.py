from libs.devices import get_devices, status_checker
from core.config import get_config

from fastapi import APIRouter
from pydantic import BaseModel


class Mac(BaseModel):
    mac: str

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

@devices.post("/status")
def get_status(mac: Mac):
    print(mac)
    status = status_checker(mac.mac, config)
    return {"status": status}
