import psycopg2
from psycopg2 import sql
from config.config import get_db_data
from services.get_valutes import get_currency_data


# Обновление данных в базе
def update_data(data) -> None:
    dbname, user, password, host, port = get_db_data()
    # переменные берутся из .env
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    cursor = conn.cursor()

    for element in data:
        cursor.execute(
            """
            INSERT INTO currency (num_code, char_code, nominal, name, value, vunit_rate)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (num_code) DO UPDATE
            SET value = EXCLUDED.value
            """,
            (element['Num_code'], element['Char_code'], element['Nominal'], element['Name'], element['Value'], element['VunitRate'])
        )

    conn.commit()
    cursor.close()
    conn.close()

# Обновляем данные о валютах в базе
update_data(get_currency_data())
