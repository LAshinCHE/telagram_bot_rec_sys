class SearchPlacesUseCase:

    def __init__(self, place_repo):
        self.place_repo = place_repo

    def execute(self, filters: dict):
        return self.place_repo.search(filters)
