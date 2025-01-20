from aiogram import Router
from aiogram.types import Message

router = Router()

# Эхо хендлер для незапланированных сообщений от пользователя
@router.message()
async def send_echo(message: Message):
    await message.answer(f'Это эхо! {message.text}, я реагирую только на команды из списка /help')