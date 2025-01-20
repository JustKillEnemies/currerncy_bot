import psycopg2
from config.config import get_db_data

# Создаем базу данных для хранения валют
def create_db():
    dbname, user, password, host, port = get_db_data()
    # Берем значения из .env файла
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
        )
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE currency (num_code SERIAL PRIMARY KEY, char_code VARCHAR(10), nominal VARCHAR(10), name varchar(50), value NUMERIC(8,4), Vunit_rate NUMERIC(10,6))"
    )

    conn.commit()
    cursor.close()
    conn.close()


create_db()
