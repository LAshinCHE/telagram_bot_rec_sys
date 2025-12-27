from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.schemas.user import (
    GetUserRequest,
    GetUserResponce,
    CreateUserRequest,
    CreateUserResponce,
)
from app.service.use_cases.user.user import UserService
from app.db.repositories.user import UserRepository


router = APIRouter(prefix="/user", tags=["user"])

# def get_user_service(
#         db: Session = Depends(get_db)
# ) -> UserService:
#     return UserService(db)

def get_user_repository(
    session: Session = Depends(get_db),
) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)

@router.post("/create", response_model=CreateUserResponce)
def create_user(
    data: CreateUserRequest,
    service: UserService = Depends(get_user_service),

):
    return service.create_user(data.id, data.name, data.role)

@router.post("/get", response_model=GetUserResponce)
def get_user(
    data: GetUserRequest,
    service: UserService = Depends(get_user_service),

):
    return service.get_user(data.id)

