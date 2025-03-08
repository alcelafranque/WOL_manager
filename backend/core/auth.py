from os import getenv

from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader, APIKey

app = FastAPI()

API_KEY = getenv("API_KEY")
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Check for api key
    """
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied",
    )
