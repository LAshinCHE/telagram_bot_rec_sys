from aiogram import Router
from aiogram.types import Message
from app.api.routes.recommendation import get_recommendation_service
from app.db.session import SessionLocal
from app.service.use_cases.llm.recommendation import Recommendation
router = Router()

# @router.message()
# async def get_places(message: Message):
#     responce = await recommend_places(data=message.text)
#     text = responce["answear"]
#     text = "\n".join(p["name"] for p in responce["places"])
#     await message.answer(text or "Ничего не найдено 😔")



@router.message()
async def get_places(message: Message):
    db = SessionLocal()
    try:
        service = get_recommendation_service(db)
        response = service.recommend(
            user_query=message.text,
            user_id=message.from_user.id,
        )
    finally:
        db.close()

    print(response)
    text = response["answer"]
    # await message.answer(response["places"])
    await message.answer(text or "Ничего не найдено")
