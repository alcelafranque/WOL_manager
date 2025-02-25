from routers.devices import devices as devices_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
# Create FastAPI instance
app = FastAPI()

# Add routers to main app
app.include_router(devices_router)

# Set CORS settings
origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    # allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["GET", "POST", "OPTIONS"]
)

2

@app.get("/")
def read_root():
    return {"message": "Welcome to WOL manager"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
