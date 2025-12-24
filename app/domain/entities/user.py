from dataclasses import dataclass
from datetime import datetime
from app.domain.enum import UserRolle

@dataclass
class User: 
    id: int
    email: str
    password_hash: str
    name: str | None
    created_at: datetime
    roles: UserRolle
