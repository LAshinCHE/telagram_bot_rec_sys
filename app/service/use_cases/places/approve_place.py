from app.exceptions import Forbidden, NotFound

class ApprovePlaceUseCase:

    def __init__(self, place_repo):
        self.place_repo = place_repo

    def execute(self, place_id: int, user):
        if user.role not in ("moderator", "admin"):
            raise Forbidden("Not enough rights")

        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise NotFound("Place not found")

        place.approve()
        return self.place_repo.save(place)