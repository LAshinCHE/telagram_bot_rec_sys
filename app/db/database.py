from app.setings import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = settings.DATABASE_URL_psycopg()

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

def healthcheck_db():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res=}")