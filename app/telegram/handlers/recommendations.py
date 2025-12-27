from aiogram import Router
from aiogram.types import Message
from app.api.routes.recommendation import recommend_places

router = Router()

@router.message()
async def get_places(message: Message):
    responce = await recommend_places(city=message.text)
    text = responce["answear"]
    text = "\n".join(p["name"] for p in responce["places"])
    await message.answer(text or "Ничего не найдено 😔")