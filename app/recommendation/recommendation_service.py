from typing import List
from surprise import SVD, Reader, Dataset
import pandas as pd
import uuid
import joblib
import json
from surprise import accuracy
from surprise.model_selection import train_test_split
from app.domain.entities.place import Place

class Recommendation:
    def __init__(self, name_model: str, name_rating_json: str):
        self.model = joblib.load(name_model)
        self.df = pd.read_json(name_rating_json)
    
    def __predict_rating(self, user_id: int, place_id: int) -> int:
        return self.model.predict(user_id, place_id).est
    
    # Функция для сортировки по популярности (если холодный старт)
    def __sort_by_popularity(self, candidates: dict[str, any]) -> dict[str, any]:
        # Сортировка по количеству отзывов, затем по среднему рейтингу
        return sorted(candidates, key=lambda x: (x['rating_cnt'], x['rating_avg']), reverse=True)

    
    def rank_places(self, user_id: int, candidates: List[dict], count_rating_user: int) -> List[dict]:
        if count_rating_user < 5:
            cold_candidates = [
                {
                    'id': place['id'],
                    'name': place['name'],
                    'description': place['description'],
                    'price_level': place['price_level'],
                    'city': place['city'],
                    'predicted_rating': None,
                    'rating_avg': place['rating_avg'],
                    'rating_cnt': place['rating_cnt']
                }
                for place in candidates
            ]
            return self.__sort_by_popularity(cold_candidates)

        predicted_places = []
        cold_start_places = []

        for place in candidates:
            place_id = place['id']
            if place['rating_cnt'] < 5:
                # Если холодный старт, сортируем по популярности
                cold_start_places.append({
                    'id': place_id,
                    'name': place['name'],
                    "description": place['description'],
                    'price_level': place['price_level'],
                    'city': place['city'],
                    'predicted_rating': None,  # нет предсказания, только сортировка по популярности
                    'rating_avg': place['rating_avg'],
                    'rating_cnt': place['rating_cnt']
                })
            else:
                # Для места с достаточным количеством оценок, используем модель для предсказания
                predicted_rating = self.__predict_rating(user_id, place_id)
                predicted_places.append({
                    'id': place_id,
                    'name': place['name'],
                    "description": place['description'],
                    'price_level': place['price_level'],
                    'city': place['city'],
                    'predicted_rating': predicted_rating,
                    'rating_avg': place['rating_avg'],
                    'rating_cnt': place['rating_cnt']
                })
        predicted_places.sort(key=lambda x: x['predicted_rating'], reverse=True)

        cold_start_places = self.__sort_by_popularity(cold_start_places)

        ranked_places = predicted_places + cold_start_places
        return ranked_places
        

    def train_model(self, name_model: str, df):
        '''
        Docstring для train_model
        :param name_model: название модели для сохранения и загрузки
        :type name_model: str
        :param df: данные для обучения модели
        '''


        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df[['user_id', 'place_id', 'rating']], reader)


        # Разделение данных на тренировочную и тестовую выборки
        trainset, testset = train_test_split(data, test_size=0.2)

        # Обучаем модель SVD
        model = SVD()
        model.fit(trainset)

        # Оценка точности на тестовых данных
        predictions = model.test(testset)
        print(f"RMSE: {accuracy.rmse(predictions)}")

        joblib.dump(model, name_model)

if __name__ == "__main__":
    # Пример кандидатов (мест)
    candidates = [
        {"id":"22222222-2222-2222-2222-222222222222","name":"Dessert House","description":"десерты и латте","city":"Moscow","price_level":3,"rating_avg":4.8,"rating_cnt":15},
        {"id":"33333333-3333-3333-3333-333333333333","name":"Noisy Coffee","description":"кофе и латте, громко","city":"Moscow","price_level":2,"rating_avg":4.7,"rating_cnt":300},
        {"id":"11111111-1111-1111-1111-111111111111","name":"Coffee Lab","description":"спешелти кофе, латте","city":"Moscow","price_level":2,"rating_avg":4.6,"rating_cnt":120},
        {"id":"44444444-4444-4444-4444-444444444444","name":"Latte & Co","description":"латте, тихо","city":"Moscow","price_level":3,"rating_avg":4.5,"rating_cnt":80},
        {"id":"55555555-5555-5555-5555-555555555555","name":"Central Roasters","description":"спешелти кофе, тихо","city":"Moscow","price_level":3,"rating_avg":4.4,"rating_cnt":40},
        {"id":"66666666-6666-6666-6666-666666666666","name":"Art Cafe","description":"кофе и десерты","city":"Moscow","price_level":2,"rating_avg":4.3,"rating_cnt":60},
        {"id":"77777777-7777-7777-7777-777777777777","name":"Morning Cup","description":"латте и выпечка","city":"Moscow","price_level":2,"rating_avg":4.1,"rating_cnt":20},
        {"id":"88888888-8888-8888-8888-888888888888","name":"Hidden Yard","description":"тихая кофейня, латте","city":"Moscow","price_level":2,"rating_avg":4.8,"rating_cnt":5},
        {"id":"99999999-9999-9999-9999-999999999999","name":"Library Coffee","description":"тихо, много места, латте","city":"Moscow","price_level":2,"rating_avg":4.6,"rating_cnt":200},
        {"id":"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa","name":"Brew & Talk","description":"кофе, разговоры","city":"Moscow","price_level":2,"rating_avg":4.2,"rating_cnt":35}
    ]
    user_id = uuid.uuid4()
    model_name = 'svd_model.pkl'
    rating_name = 'ratings_data.json'
    rec = Recommendation(model_name, rating_name)
    ranked_places = rec.rank_places(user_id, candidates, 2)
    with open('Recomndation_output.json', 'w', encoding='utf-8') as f:
        json.dump(ranked_places, f, ensure_ascii=False, indent=2)