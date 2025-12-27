from pydantic import BaseModel
from app.domain.enum import UserRole

class GetUserRequest(BaseModel):
  id: int

class GetUserResponce(BaseModel):
  name: str
  role: UserRole

class CreateUserRequest(BaseModel):
  id: int
  name: str
  role: UserRole

class CreateUserResponce(BaseModel):
  id: int