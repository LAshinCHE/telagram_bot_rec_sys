from app.repositories.models import * 
from app.repositories.database import engine, Base 
from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Places API")

app.include_router(api_router)

def main():
    print("Starting application")

    print("Creating databses tables...")
    Base.metadata.create_all(bind=engine)
    print("Databases tables create!!!!")

if __name__ == '__main__':
    main()