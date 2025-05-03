from fastapi import FastAPI
from starwars_api.routers import v1

# Create the main application (acts as a dispatcher)
app = FastAPI(
    title="Root Star Wars API",
    version="root",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

# Create versioned sub-app with its own docs
v1_app = FastAPI(
    title="Star Wars API v1",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Include the v1 router in the v1 sub-app
v1_app.include_router(v1.router)

# Mount the v1 sub-app
app.mount("/api/v1", v1_app)