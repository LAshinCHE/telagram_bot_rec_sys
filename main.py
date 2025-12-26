from app.db.models import *
from app.db.database import engine, Base
from fastapi import FastAPI
from app.api.router import api_router
import uvicorn

app = FastAPI(title="Places API")

app.include_router(api_router)

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created!")

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(
        "main:app",           
        host="0.0.0.0",       
        port=8000,
        reload=True          
    )
