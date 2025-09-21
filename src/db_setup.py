import time

import psycopg2

from src.utils import get_env_variable


def create_database_and_tables():
    db_name = get_env_variable("DB_NAME").strip()
    user = get_env_variable("DB_USER").strip()
    password = get_env_variable("DB_PASSWORD").strip()
    host = get_env_variable("DB_HOST").strip()
    port = int(get_env_variable("DB_PORT").strip())

    # Подключаемся к postgres для создания БД
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {db_name};")
        print(f"База {db_name} создана")
    else:
        print(f"База {db_name} уже существует")

    cur.close()
    conn.close()

    # Даем серверу 2 секунды на регистрацию базы
    time.sleep(2)

    # Подключаемся к нашей базе
    with psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port) as conn:
        with conn.cursor() as cur:
            # Создание таблиц
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    employer_id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url TEXT
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id INT PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    title VARCHAR(255) NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    url TEXT
                );
            """)
        conn.commit()
        print("Таблицы созданы или уже существуют")
