from fastapi import APIRouter
from fastapi import FastAPI

def create_service() -> FastAPI:
    app = FastAPI()
    return app

def create_router() -> APIRouter:
    router = APIRouter()
    return router