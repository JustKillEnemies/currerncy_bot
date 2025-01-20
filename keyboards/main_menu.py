from aiogram import Bot
from aiogram.types import BotCommand

# Установка главного меню бота
async def set_main_menu(bot: Bot):
    # Список команд
    main_menu_commands = [
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='currency', description='Валюты'),
        BotCommand(command='calculator', description="Калькулятор валют"),
        BotCommand(command='codes', description="Список кодов валют"),
        BotCommand(command='cancel', description="Отмена действия")
    ]

    await bot.set_my_commands(main_menu_commands)