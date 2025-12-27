# from dataclasses import dataclass

# @dataclass
# class Tag:
#     id: int
#     name: str

from pydantic import BaseModel

class Tag(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # важно для SQLAlchemy
