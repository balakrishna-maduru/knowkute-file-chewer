# Entry point for FastAPI app


from fastapi import FastAPI
from .config import *
from app.routes.file_routes import router as file_router
from app.routes.health_routes import router as health_router

app = FastAPI(title="Knowkute File Chewer")

app.include_router(file_router)
app.include_router(health_router)

@app.get("/")
def root():
    return {"message": "Welcome to Knowkute File Chewer API"}
