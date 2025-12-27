# Places Recommendation System
---
Places Recommendation System - телеграмм бот для поиска мест, чтобы провести свой досуг



Система позволяет:
- хранить и управлять базой мест (кафе, развлечения, досуг и т.д.);

- автоматически формировать рекомендации;

- использовать LLM для генерации ответов и суммаризации отзывов;

- интегрироваться с внешними источниками (Telegram-каналы, веб-порталы).

Проект реализован с упором на Domain-Driven Design (DDD) и четкое разделение слоев ответственности.


```
app/
├── api/                # FastAPI routes
│
├── domain/             # Струрктуры 
│
├── service/            # Use-cases основная логика приложение 
│
├── db/                 # ORM, репозитории
│
├── recommendation/     # Алгоритмы сортировки мест по атрибутам
│
├── llm/                # Интеграция с LLM
│
├── telegram/           # Интеграция с Telegram
│
├── settings.py         # Конфигурация приложения
├── config.py
└── main.py             # Точка входа

```

## Архитектура базы данных
#### Пользователи и роли:

users: id, email, password_hash, name, role(user|moderator|admin),  created_at

#### Места и фильтрация:

places: id, name, description, city, address_text, price_level, status(pending|active|rejected|archived), created_by, created_at, updated_at

tags: id, name

place_tags: place_id, tag_id

place_stats: place_id, rating_avg, rating_cnt, reviews_cnt, updated_at


#### Отзывы и оценки (с модерацией):

ratings: user_id, place_id, rating(1..5), created_at, updated_at

reviews: id, place_id, author_id, rating(1..5), text, status(pending|approved|rejected), moderated_by, moderated_at, created_at



#### Рекомендации :

reco_model_versions: id, algo, trained_at, metrics_json, artifact_uri

user_recommendations: user_id, place_id, score, model_version_id, generated_at