from db.repositories.reviews import ReviewRepository
from app.recomendation.recomendation_service import Recomendation

class  RecomendationService:
    def __init__(self, recomendation_repo: ReviewRepository, recomendation : Recomendation):
        self.recomendation = recomendation
        self.recomendation_repo = recomendation_repo
        
    def train_model(self, name_model: str):
        df = self.recomendation_repo.get_reviews()
        self.recomendation.train_model()

    def get_rank_place(self):
        self.recomendation.rank_place()