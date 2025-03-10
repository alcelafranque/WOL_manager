from core.auth import get_api_key
from core.config import get_config
from schemas.devices import Device
from workers.status_checker import StatusChecker

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.api_key import APIKey

devices = APIRouter(
    prefix="",
    tags=["devices"]
)

# Get config
config = get_config()

# Create status checker instance
status_checker = StatusChecker(config["network"])


@devices.get("/devices")
def retrieve_devices(api_key: APIKey = Depends(get_api_key)):
    devices = Device.get_devices()
    status_checker.devices = devices
    return {"devices": devices}


@devices.post("/status")
def get_status(device: Device, api_key: APIKey = Depends(get_api_key)):
    status = status_checker.devices_status[device.mac]
    return {"status": status}


@devices.post("/start")
def start_device(device: Device, api_key: APIKey = Depends(get_api_key)):
    device.start()
    return


@devices.post("/register")
def register_device(device: Device, api_key: APIKey = Depends(get_api_key)):
    status_code = device.register()

    if status_code != 200:
        raise HTTPException(status_code=status_code)

    return


@devices.post("/delete")
def delete_device(device: Device, api_key: APIKey = Depends(get_api_key)):
    device.delete()
    return


@devices.post("/update")
def update_device(device: Device, api_key: APIKey = Depends(get_api_key)):
    device.update()
    return