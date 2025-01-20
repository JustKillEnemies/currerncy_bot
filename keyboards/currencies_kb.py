from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.database_get import get_data


# Функция для создания клавиатуры с кнопками для выбора валют
def create_currencies_keyboard() -> InlineKeyboardMarkup:
    vals = get_data()  # Получаем данные о валютах (например, из базы данных или API)
    kb_builder = InlineKeyboardBuilder()  # Создаем объект для построения клавиатуры

    # Разбиваем список данных на строки по 4 элемента и добавляем кнопки на клавиатуру
    for i in range(0, 43, 4):
        # Создаем строку клавиатуры, добавляя по 4 кнопки за раз
        kb_builder.row(*[
            InlineKeyboardButton(
                text=element.get('Char_code'),  # Текст на кнопке - это код валюты
                callback_data=element.get('Char_code'),  # Данные для обратного вызова при нажатии - код валюты
            )
            for element in vals[i:i+4]  # Обрабатываем 4 элемента за раз
        ])

    return kb_builder.as_markup()  # Генерируем клавиатуру и возвращаем её в формате Telegram

