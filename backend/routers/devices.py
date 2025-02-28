from libs.devices import get_devices

from fastapi import APIRouter

devices = APIRouter(
    prefix="",
    tags=["devices"]
)

@devices.get("/devices")
def retrieve_devices():
    devices = get_devices()
    return {"devices": devices}
