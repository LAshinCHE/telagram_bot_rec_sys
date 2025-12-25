from fastapi import FastAPI

def create_service() -> FastAPI:
    app = FastAPI()
    return app