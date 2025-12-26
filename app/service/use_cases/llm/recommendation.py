from typing import List
from app.db.repositories.reviews import ReviewRepository
from app.recommendation.recommendation_service import Recommendation
from app.domain.entities.place import Place
from app.domain.entities.review import Review
from app.db.models.place import Place
from app.llm.llm_entities import LLM_Entities
from app.llm.llm_generation_answer import LLM_Generation
from app.db.repositories.place import PlaceRepository

class RecommendationService:
    def __init__(
        self,
        recommendation_repo: ReviewRepository,
        place_repo: PlaceRepository,
        recommendation: Recommendation,
        llm_entities: LLM_Entities,
        generation_llm: LLM_Generation
    ):
        self.recommendation_repo = recommendation_repo
        self.place_repo = place_repo
        self.recommendation = recommendation
        self.llm_entities = llm_entities
        self.generation_llm = generation_llm

        
    def train_model(self, name_model: str):
        df = self.recommendation_repo.get_reviews()
        self.recommendation.train_model("svd_model.pkl", df)

    def get_rank_place(self, user_id: int, candidates: list[Place]) -> list[Place]:
        '''
        :param user_id: id пользователя, для которого нужно предложить места.
        :type user_id: int
        :param candidates: места отобранные по тегам
        :type candidates: list[dict]
        '''
        count_rating_user = self.recommendation_repo.get_count_rating_user(user_id)
        ranking_places = self.recommendation.rank_places(user_id, candidates, count_rating_user)
        return ranking_places
    
    def recommend(self, user_query: str, user_id : int) -> dict:
        filters = self.llm_entities.extract_filters_openai(user_query)

        places = self.place_repo.search_places(
            city=filters["city"],
            price_level=filters["price_level"],
            include_tags=filters["selected_tags"],
        )

        candidates = self.place_repo.make_

        ranked = self.recommendation.rank_places(user_id, places)

        ans = self.generation_llm.generation(ranked)

        return ans

    def _rank_places(self, places: List[Place], filters: dict):
        result = []

        for place in places:
            score = 0.0

            if place.stats and place.stats.rating_avg:
                score += place.stats.rating_avg * 2

            place_tags = {t.name for t in place.tags}
            must = set(filters["must_have"])
            nice = set(filters["nice_to_have"])

            score += len(place_tags & must) * 3
            score += len(place_tags & nice) * 1

            result.append((score, place))

        result.sort(key=lambda x: x[0], reverse=True)

        return [self._serialize_place(p) for _, p in result]

    def _serialize_place(self, place: Place):
        return {
            "id": place.id,
            "name": place.name,
            "city": place.city,
            "price_level": place.price_level,
            "rating_avg": place.stats.rating_avg if place.stats else None,
            "rating_cnt": place.stats.rating_cnt if place.stats else 0,
            "tags": [t.name for t in place.tags],
        }
