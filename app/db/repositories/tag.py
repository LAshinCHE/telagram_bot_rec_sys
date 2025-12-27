from app.service.interfaces.repositories.tag_repo import TagRepositoryI
from sqlalchemy.orm import Session
from app.db.models import Tag as TagModel
from app.domain.entities.tag import Tag as TagEntity

class TagRepository(TagRepositoryI):
    def __init__(self, session: Session):
        self.session = session
    
    def fill(self, names: list[str]):
        counter = 0
        for name in names:
            new_tag_db = TagModel(name=name) 
            self.session.add(new_tag_db)
        
        # Делаем commit после цикла для производительности (или внутри, если нужно сразу)
        self.session.commit()
    
    def get_all(self) -> list[TagEntity]:
        all_tags = self.session.query(TagModel).all()
        our_tags = []
        for i in all_tags:
            tag = TagEntity(
                id=i.id,
                name=i.name
            )
            our_tags.append(tag)
        print(all_tags)
        if not all_tags:
            return None

        return our_tags
    
    def get_by_id(self, id: int) -> TagEntity:
        raw_tag = self.session.query(TagModel).filter_by(id=id).first()
        return TagEntity(id=raw_tag.id, name=raw_tag.name)
    
    def get_by_name(self, name: str) -> TagEntity:
        raw_tag = self.session.query(TagModel).filter_by(name=name).first()
        return TagEntity(id=raw_tag.id, name=raw_tag.name)
    