from app.db.database import healthcheck_db


def healthcheck_service() -> dict:
    db_ok = healthcheck_db()

    status = "ok" if db_ok else "degraded"

    return {
        "status": status,
        "components": {
            "database": "ok" if db_ok else "down",
            "api": "ok"
        }
    }
