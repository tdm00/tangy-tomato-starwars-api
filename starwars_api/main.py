from fastapi import FastAPI
from starwars_api.routers import v1, v2, v3

# Root app (no docs here, only mounts)
app = FastAPI(
    title="Root Star Wars API",
    version="root",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

# Version 1 sub-app
v1_app = FastAPI(
    title="Star Wars API v1",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
v1_app.include_router(v1.router)
app.mount("/api/v1", v1_app)

# Version 2 sub-app
v2_app = FastAPI(
    title="Star Wars API v2",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
v2_app.include_router(v2.router)
app.mount("/api/v2", v2_app)

# Version 3 sub-app
v3_app = FastAPI(
    title="Star Wars API v3",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
v3_app.include_router(v3.router)
app.mount("/api/v3", v3_app)
