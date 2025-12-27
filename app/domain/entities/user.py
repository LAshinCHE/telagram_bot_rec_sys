from dataclasses import dataclass
from datetime import datetime
from app.domain.enum import UserRole

@dataclass
class User: 
    id: int
    name: str | None
    created_at: datetime
    role: UserRole
