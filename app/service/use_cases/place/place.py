from app.service.interfaces.repositories.place_repo import PlaceRepositoryI
from app.domain.entities.place import Place
from app.exceptions.exceptions import NotFound, Forbidden

class PlaceService:
    def __init__(self, place_repo: PlaceRepositoryI):
        self.place_repo = place_repo
    
    def create_place(self, place : Place):
        return self.place_repo.save(place)
    

    def get_place(self, place_id: int) -> Place:
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise NotFound("Place not found")
        return place
    
    def search_place(self, filters: dict):
        return self.place_repo.search_places(
        city=filters.get("city"),
        price_level=filters.get("price_level"),
        include_tags=filters.get("selected_tags")
        )
    

    def approve_place(self, place_id: int, user):
        if user.role not in ("moderator", "admin"):
            raise Forbidden("Not enough rights")

        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise NotFound("Place not found")

        place.approve()
        return self.place_repo.save(place)