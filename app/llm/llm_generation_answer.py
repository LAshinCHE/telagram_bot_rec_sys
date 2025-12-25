import sys
import io
from openai import OpenAI
import json
from typing import Any, Dict, List, Optional

class LLM_Generation:
    def __init__(self, LM_STUDIO_URL: str, API_KEY: str, MODEL_NAME: str):
        self.LM_STUDIO_URL = LM_STUDIO_URL
        self.API_KEY = API_KEY
        self.MODEL_NAME = MODEL_NAME
        self.client =OpenAI(base_url=LM_STUDIO_URL, api_key=API_KEY)

        self.SYSTEM_PROMPT: str = """Ты — помощник, который создает естественные ответы на русском языке о рекомендованных заведениях.
        Твоя задача: на основе списка рекомендованных мест с их описаниями, рейтингами и отзывами создать красивый, естественный ответ на русском языке.

        ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА:
        1) Верни строго один JSON-объект с полем "answer" содержащим текст ответа на русском языке.
        2) Ответ должен быть естественным, дружелюбным и информативным.
        3) Упомяни названия мест, их особенности из описаний, рейтинги.
        4) Структурируй ответ так, чтобы он был читаемым и полезным для пользователя.
        5) Используй информацию о рейтингах и количестве отзывов для придания авторитетности рекомендациям.

        СХЕМА ОТВЕТА (строго эти ключи):
        {
          "answer": string
        }

        Никакого Markdown, списков, пояснений, комментариев или текста вокруг JSON. Только чистый JSON.
        """
    
    def __get_place_descriptions_from_db(place_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Получает описания мест из базы данных по их ID.
        Возвращает словарь {place_id: {name, description, city, price_level, rating_avg, rating_cnt, reviews}}
        """
        return "bb"
    
    def __build_user_prompt(self, places_data: List[Dict[str, Any]]) -> str:
        """
        Создает промпт для LLM на основе данных о местах.
        """
        payload = {
            "PLACES": places_data,
            "INSTRUCTIONS": "Создай естественный ответ на русском языке о рекомендованных местах. "
                           "Используй информацию о названиях, описаниях, рейтингах и отзывах. "
                           "Ответ должен быть дружелюбным и информативным.",
            "OUTPUT": "Return JSON only with 'answer' field containing the natural language response."
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
    
    def __generate_answer_openai(
        self,
        places_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Вызывает LLM для генерации естественного ответа о рекомендованных местах.
        """
        user_prompt = self.__build_user_prompt(places_data)

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        text = (resp.choices[0].message.content or "").strip()
    
        # Убираем markdown форматирование если есть
        if text.startswith("```"):
            text = text.strip("`").replace("json", "", 1).strip()
    
        if not text:
            raise RuntimeError("Empty model response")
    
        # Парсим JSON
        try:
            obj = json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Model did not return valid JSON. Raw: {text}") from e
    
        # Проверяем наличие поля answer
        if "answer" not in obj:
            raise ValueError("Response missing 'answer' field")
    
        return obj

    def generation(self, file_rec_json: str) -> Dict[str, Any]:
        """
        Основная функция: загружает рекомендации, получает описания из БД, генерирует ответ через LLM.
        """
        # Загружаем рекомендованные места из JSON
        try:
            with open('Recomndation_1_output.json', 'r', encoding='utf-8') as f:
                recommendations_data = json.load(f)
        except FileNotFoundError:
            print("Ошибка: файл Recomndation_1_output.json не найден")
            return
        except json.JSONDecodeError as e:
            print(f"Ошибка при чтении JSON: {e}")
            return
        
        recommended_places = recommendations_data.get('recommended_places', [])

        if not recommended_places:
            print("Нет рекомендованных мест для обработки")
            return
        
        place_ids = [place['id'] for place in recommended_places]

        db_descriptions = self.__get_place_descriptions_from_db(place_ids)

        # Объединяем данные из рекомендаций с данными из БД
        places_data = []
        for place in recommended_places:
            place_id = place['id']
            db_info = db_descriptions.get(place_id, {})

            # Объединяем данные: приоритет у данных из БД, но используем данные из рекомендаций если БД нет
            place_info = {
                'id': place_id,
                'name': db_info.get('name') or place.get('name', ''),
                'description': db_info.get('description', ''),
                'city': db_info.get('city', ''),
                'price_level': db_info.get('price_level'),
                'rating_avg': db_info.get('rating_avg') or place.get('rating_avg'),
                'rating_cnt': db_info.get('rating_cnt') or place.get('rating_cnt', 0),
                'predicted_rating': place.get('predicted_rating'),
                'reviews': db_info.get('reviews', [])
            }
            places_data.append(place_info)
        
        try:
            answer_result = self.__generate_answer_openai(places_data)

            # Сохраняем результат в JSON
            output_data = {
                "answer": answer_result.get("answer", ""),
                "places_count": len(places_data),
                "places": places_data
            }

            return output_data
        
        except Exception as e:
            print(f"Ошибка при генерации ответа: {e}")
            return None

if __name__ == "__main__":
    LM_STUDIO_URL = "http://127.0.0.1:1234/v1"
    API_KEY = "lm-studio"
    MODEL_NAME = "openai/gpt-oss-20b"
    gen = LLM_Generation(LM_STUDIO_URL=LM_STUDIO_URL, API_KEY=API_KEY, MODEL_NAME=MODEL_NAME)

    output_data = gen.generation("Recomndation_1_output.json")

    output_file = "Answer_output.json"

    with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
