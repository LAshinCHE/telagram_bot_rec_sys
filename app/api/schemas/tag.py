from pydantic import BaseModel
from app.domain.entities.tag import Tag as TagEntity


class CreateTagRequest(BaseModel):
    pass

class CreateTagResponse(BaseModel):
    pass

class GetAllTagsReques(BaseModel):
    pass

class GetAllTagsResponse(BaseModel):
    items: list[TagEntity]

class GetTagByNameRequest(BaseModel):
    name: str

class GetTagByNameResponse(BaseModel):
    name: str
    id: int

class GetTagByIdRequest(BaseModel):
    id: int

class GetTagByIdResponse(BaseModel):
    name: str
    id: int