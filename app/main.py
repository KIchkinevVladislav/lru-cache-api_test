import uvicorn
from fastapi import FastAPI

from api.api import cache_routers
from app.middleware import log_request_time

app = FastAPI()

app.middleware("http")(log_request_time)

app.include_router(cache_routers, prefix="/cache", tags=["cache"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
