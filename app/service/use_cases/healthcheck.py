from app.repositories.database import healthcheck_db

def service_healthcheck():
    healthcheck_db()