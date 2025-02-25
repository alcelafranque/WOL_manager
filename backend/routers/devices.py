from fastapi import APIRouter

devices = APIRouter(
    prefix="",
    tags=["devices"]
)

@devices.get("/devices")
def get_devices():
    return {"message": "OK"}
