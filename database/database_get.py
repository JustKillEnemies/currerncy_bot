import psycopg2
from psycopg2 import sql
from config.config import get_db_data


# получаем все данные о валютах в виде списка из словарей
def get_data() -> list[dict[str, str]]:
    dbname, user, password, host, port = get_db_data()

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM currency")
    rows = cursor.fetchall()

    result = [convert_to_dict(row) for row in rows]

    cursor.close()
    conn.close()

    return result


# преобразуем каждую валюту в словарь
def convert_to_dict(row):
    data_dict = {
        "Char_code": row[1],
        "Nominal": row[2],
        "Name": row[3],
        "Value": str(row[4]),  # Преобразуем Decimal в строку
        "VunitRate": str(row[5])
    }
    return data_dict


# получаем столбик из всех кодов валют
def get_codes(data):
    result = []
    for curr in data:

        result.append(f"{curr['Char_code']} - {curr['Name']}")

    return '\n'.join(result)


# Переменная, которая хранит все коды валют
codes = get_codes(get_data())
