from fastapi import FastAPI
from starwars_api.routers import v1

app = FastAPI(title="Star Wars API")

app.include_router(v1.router, prefix="/api/v1", tags=["v1"])
