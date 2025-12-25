import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise import accuracy
from surprise.model_selection import train_test_split
import joblib

class TrainRecomendationModel:

    def __get_data_from_db(self,) -> pd:
        '''
        Здесь должно быть обращение в бд, чтобы получить
        все рейтинги
        '''
        pass

    def __prepare_data_for_training(self, df: pd) -> Dataset:
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df[['user_id', 'place_id', 'rating']], reader)
        return data
    
    def __train_model(self, data: Dataset):
        # Разделение данных на тренировочную и тестовую выборки
        trainset, testset = train_test_split(data, test_size=0.2)

        # Обучаем модель SVD
        model = SVD()
        model.fit(trainset)

        # Оценка точности на тестовых данных
        predictions = model.test(testset)
        print(f"RMSE: {accuracy.rmse(predictions)}")

        return model
    
    def __save_model(model, model_filename='svd_model.pkl'):
        joblib.dump(model, model_filename)

    def train_model(self, name_model: str):
        df = self.__get_data_from_db()

        data = self.__prepare_data_for_training(df)

        model = self.__train_model(data)

        self.__save_model(model, name_model)

if __name__ == "__main__":
    train = TrainRecomendationModel()
    train.train_model('svd_model.pkl')