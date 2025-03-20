import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .company_routes import router

app = FastAPI()

static_dir = os.path.join(os.path.dirname(__file__), "static")

# Ensure static directory exists
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Mount static directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Register the router
app.include_router(router)

from . import company_routes
