# Entry point for FastAPI app

from fastapi import FastAPI
from .config import *

app = FastAPI(title="Knowkute File Chewer")

# Routers will be included here
# from .routes import file_routes, query_routes, health_routes
# app.include_router(file_routes.router)
# app.include_router(query_routes.router)
# app.include_router(health_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Knowkute File Chewer API"}
