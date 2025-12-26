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
            model=self.MODEL_NAME,
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

    def generation(self, recommended_places) -> Dict[str, Any]:
        """
        Основная функция: загружает рекомендации, получает описания из БД, генерирует ответ через LLM.
        """
        
        try:
            answer_result = self.__generate_answer_openai(recommended_places)

            # Сохраняем результат в JSON
            output_data = {
                "answer": answer_result.get("answer", ""),
                "places_count": len(recommended_places),
                "places": recommended_places
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

    output_data = gen.generation(candidates)

    output_file = "Answer_output.json"

    with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
