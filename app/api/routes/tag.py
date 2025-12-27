from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.schemas.tag import (
    GetAllTagsResponse,
    GetTagByIdRequest,
    GetTagByIdResponse,
    GetTagByNameRequest,
    GetTagByNameResponse,
)
from app.service.use_cases.tag.tag import TagService
from app.db.repositories.tag import TagRepository

router = APIRouter(prefix="/tag", tags=["tag"])

def get_tag_repository(
    session: Session = Depends(get_db),
) -> TagRepository:
    return TagRepository(session)


def get_tag_service(
    user_repo: TagRepository = Depends(get_tag_repository),
) -> TagService:
    return TagService(user_repo)

@router.post("/create")
def create_tags(
    service: TagService = Depends(get_tag_service),
):
    return service.create_tag()

@router.post("/get_all", response_model=GetAllTagsResponse)
def get_all(
    service: TagService = Depends(get_tag_service),
):
    tags = service.get_all_tags()
    return GetAllTagsResponse(items=tags)

@router.post("/get_by_id", response_model=GetTagByIdResponse)
def get_by_id(
    data: GetTagByIdRequest,
    service: TagService = Depends(get_tag_service),
):
    return service.get_by_id(data.id)

@router.post("/get_by_name", response_model=GetTagByNameResponse)
def get_by_id(
    data: GetTagByNameRequest,
    service: TagService = Depends(get_tag_service),
):
    return service.get_by_name(data.name)
