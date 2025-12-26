import json
from typing import Any, Dict, List
from openai import OpenAI 

class LLM_Entities:
    def __init__(
        self,
        LM_STUDIO_URL: str,
        API_KEY: str,
        ALLOWED_TAGS: List[str],
        DEFAULT_MODEL: str,
    ):
        self.LM_STUDIO_URL = LM_STUDIO_URL
        self.API_KEY = API_KEY
        self.ALLOWED_TAGS = ALLOWED_TAGS
        self.DEFAULT_MODEL = DEFAULT_MODEL

        self.EXPECTED_KEYS: List[str] = [
            "city",
            "price_level",
            "must_have",
            "nice_to_have",
            "selected_tags",
            "excluded_tags",
            "free_text_query",
            "confidence",
        ]

        self.PRICE_LEVEL_RULE: str = """- If user says "дёшево/недорого/бюджетно" => price_level = 1
        - If user says "средний чек/умеренно/не слишком дорого" => price_level = 2
        - If user says "дорого" => price_level = 3
        - If user says "премиум/очень дорого" => price_level = 4
        - Otherwise => null"""

        self.SYSTEM_PROMPT: str = """Ты — компонент извлечения структурированных фильтров для поиска заведений (places).
        Твоя задача: по тексту пользователя выделить требования и вернуть их в виде JSON строго по заданной схеме.
        
        ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА:
        1) Верни строго один JSON-объект. Никакого Markdown, списков, пояснений, комментариев или текста вокруг JSON.
        2) Ты можешь использовать только теги из списка ALLOWED_TAGS, который будет передан в пользовательском сообщении.
              - Если нужного тега нет в ALLOWED_TAGS, не придумывай новый тег. Вместо этого добавь смысл в поле free_text_query.
        3) Если пользователь явно исключает что-то (например: “не бар”, “без шумно”, “не хочу кальян”), добавь соответствующий тег в excluded_tags.
        4) Разделяй требования на:
           - must_have: критично (без этого запрос не удовлетворяется)
           - nice_to_have: предпочтительно (желательно, но необязательно)
           Все элементы must_have и nice_to_have должны быть тегами из ALLOWED_TAGS.
        5) selected_tags — это объединение must_have и nice_to_have, без дублей.
        6) Если город не указан — city = null. Если указан неоднозначно — выбери наиболее вероятный вариант или city=null и перенеси текст в free_text_query.
        7) price_level заполняй числом 1..4 согласно правилу PRICE_LEVEL_RULE (будет передано пользователем). Если не уверен — null.
        8) confidence — число от 0.0 до 1.0: насколько уверенно ты сопоставил запрос тегам и цене.

        СХЕМА ОТВЕТА (строго эти ключи):
        {
          "city": string|null,
          "price_level": number|null,
          "must_have": string[],
          "nice_to_have": string[],
          "selected_tags": string[],
          "excluded_tags": string[],
          "free_text_query": string,
          "confidence": number
        }
        """

    @staticmethod
    def _dedupe_keep_order(items: List[str]) -> List[str]:
        seen = set()
        out = []
        for x in items:
            if x not in seen:
                out.append(x)
                seen.add(x)
        return out

    def validate_and_normalize(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the raw JSON returned by the LLM and normalise it.
        """
        # Ensure all expected keys are present
        for k in self.EXPECTED_KEYS:
            if k not in obj:
                raise ValueError(f"Missing key: {k}")

        # City
        city = obj["city"]
        if city is not None and not isinstance(city, str):
            raise ValueError("city must be string or null")

        # Price level
        price_level = obj["price_level"]
        if price_level is not None:
            if not isinstance(price_level, (int, float)):
                raise ValueError("price_level must be number or null")
            price_level = int(price_level)
            if price_level < 1 or price_level > 4:
                raise ValueError("price_level must be in 1..4 or null")

        # Helper to normalise tag lists
        def norm_tags(x: Any) -> List[str]:
            if x is None:
                return []
            if not isinstance(x, list) or not all(isinstance(t, str) for t in x):
                raise ValueError("tag lists must be string[]")
            x = [t.strip() for t in x if t.strip()]
            return self._dedupe_keep_order([t for t in x if t in set(self.ALLOWED_TAGS)])

        must_have = norm_tags(obj["must_have"])
        nice_to_have = norm_tags(obj["nice_to_have"])
        excluded = norm_tags(obj["excluded_tags"])

        selected = self._dedupe_keep_order(must_have + nice_to_have)

        free_text = obj["free_text_query"] or ""
        if not isinstance(free_text, str):
            raise ValueError("free_text_query must be string")

        conf = obj["confidence"]
        if not isinstance(conf, (int, float)):
            raise ValueError("confidence must be number")
        conf = max(0.0, min(float(conf), 1.0))

        return {
            "city": city,
            "price_level": price_level,
            "must_have": must_have,
            "nice_to_have": nice_to_have,
            "selected_tags": selected,
            "excluded_tags": excluded,
            "free_text_query": free_text.strip(),
            "confidence": conf,
        }

    def build_user_prompt(self, user_query: str) -> str:
        """
        Build the user message sent to the LLM.
        """
        payload = {
            "USER_QUERY": user_query,
            "ALLOWED_TAGS": self.ALLOWED_TAGS,
            "PRICE_LEVEL_RULE": self.PRICE_LEVEL_RULE,
            "OUTPUT": "Return JSON only.",
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def extract_filters_openai(
        self,
        user_query: str,
        *,
        client: OpenAI | None = None,
        model: str | None = None,
        temperature: float = 0.0,
    ) -> Dict[str, Any]:
        if client is None:
            client = OpenAI(base_url=self.LM_STUDIO_URL, api_key=self.API_KEY)

        if model is None:
            model = self.DEFAULT_MODEL

        user_prompt = self.build_user_prompt(user_query)
        resp = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = (resp.choices[0].message.content or "").strip()

        # Strip Markdown fences if present
        if text.startswith("```"):
            text = text.strip("`").replace("json", "", 1).strip()

        if not text:
            raise RuntimeError("Empty model response")

        try:
            obj = json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Model did not return valid JSON. Raw: {text}") from e

        return self.validate_and_normalize(obj)

# --------------------------------------------------------------------
# Example usage
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Define the tag list once
    ALLOWED_TAGS: List[str] = [
        # Type
        "ресторан","кафе","кофейня","бар","паб","клуб","столовая","фастфуд","пиццерия","бургерная","суши-бар",
        "кондитерская","пекарня","кальянная","винный бар","коктейль-бар","караоке","фудкорт","гастробар",
        # Cuisine
        "русская","европейская","итальянская","французская","испанская","греческая","американская","мексиканская",
        "латиноамериканская","грузинская","армянская","турецкая","ближневосточная","израильская","азиатская",
        "китайская","японская","корейская","тайская","вьетнамская","индийская","паназиатская","средиземноморская",
        # Drinks & specialization
        "кофе-спешиалти","кофе-to-go","чайная","bubble tea","крафтовое пиво","пивоварня","вино","дегустации",
        "авторские коктейли","настойки","безалкогольные коктейли",
        # Diet
        "вегетарианское","веганское","безглютеновое","безлактозное","халяль","кошер","постное меню","здоровое питание",
        # Occasions
        "завтрак","бранч","бизнес-ланч","ужин","поздний ужин","свидание","с друзьями","семейное","день рождения",
        "банкет","корпоратив","мероприятия","живая музыка","квизы","настольные игры",
        # Atmosphere
        "уютно","тихо","шумно","романтично","панорамный вид","терраса","камин","современно","лофт","атмосферно",
        "авторская кухня","необычный интерьер",
        # Work
        "можно с ноутбуком","много розеток","быстрый Wi-Fi","коворкинг-зона","тихая зона","удобные столы",
        # Family
        "детское меню","детская комната","детские стульчики","подходит с коляской","семейные столы",
        # Accessibility & comfort
        "доступная среда","безбарьерный вход","лифт","туалет для маломобильных","кондиционер","гардероб",
        "оплата картой","оплата QR","бронирование","доставка","самовывоз",
        # Pets
        "pet-friendly","миска для воды","можно с собакой",
    ]

    entities = LLM_Entities(
        LM_STUDIO_URL="http://127.0.0.1:1234/v1",
        API_KEY="lm-studio",
        ALLOWED_TAGS=ALLOWED_TAGS,
        DEFAULT_MODEL="openai/gpt-oss-20b",
    )

    example_query = (
        "Хочу уютную кофейню, чтобы можно было поработать с ноутбуком, тихо, и недорого. "
        "Не бар. В Москве."
    )
    result = entities.extract_filters_openai(example_query)
    print(json.dumps(result, ensure_ascii=False, indent=2))