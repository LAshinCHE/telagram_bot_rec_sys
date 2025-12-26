from db.repositories.reviews import ReviewRepository
from app.recomendation.recomendation_service import Recomendation
from app.domain.entities.place import Places

class  RecomendationService:
    def __init__(self, recomendation_repo: ReviewRepository, recomendation : Recomendation):
        self.recomendation = recomendation
        self.recomendation_repo = recomendation_repo
        
    def train_model(self, name_model: str):
        df = self.recomendation_repo.get_reviews()
        self.recomendation.train_model("svd_model.pkl", df)

    def get_rank_place(self, user_id: int, candidates: list[Places]) -> list[Places]:
        '''
        :param user_id: id пользователя, для которого нужно предложить места.
        :type user_id: int
        :param candidates: места отобранные по тегам
        :type candidates: list[dict]
        '''
        count_rating_user = self.recomendation_repo.get_count_rating_user(user_id)
        self.recomendation.rank_place()