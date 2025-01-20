from environs import Env
from dataclasses import dataclass


# Класс для хранения информации о Telegram-боте
@dataclass
class TgBot:
    token: str  # Токен для доступа к API Telegram


# Класс для конфигурации, включающий объект TgBot
@dataclass
class Config:
    tg_bot: TgBot  # Экземпляр класса TgBot, содержащий информацию о боте


# Функция для загрузки конфигурации из .env файла
def load_config(path: str | None = None) -> Config:
    env = Env()  # Создаем объект Env для работы с переменными окружения
    env.read_env(path)  # Читаем переменные из файла .env (если путь указан)

    # Возвращаем объект Config с данными для бота, используя данные из окружения
    return Config(
        tg_bot=TgBot(
            token=env('token')  # Извлекаем токен из переменной окружения
        )
    )


# Функция для получения данных о базе данных из .env файла
def get_db_data(path: str | None = None):
    env = Env()  # Создаем объект Env для работы с переменными окружения
    env.read_env(path)  # Читаем переменные из файла .env (если путь указан)

    # Возвращаем список данных для подключения к базе данных
    return [env("dbname"), env('user'), env("password"), env('host'), env('port')]  # Извлекаем данные для подключения
