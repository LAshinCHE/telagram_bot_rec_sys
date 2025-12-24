from app.exceptions import NotFound

class GetPlaceUseCase:

    def __init__(self, place_repo):
        self.place_repo = place_repo

    def execute(self, place_id: int):
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise NotFound("Place not found")
        return place
