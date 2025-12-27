from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.database import Base
from enum import Enum
from app.domain.enum import UserRole

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    role = mapped_column(String(20), nullable=False, default=UserRole.USER)

