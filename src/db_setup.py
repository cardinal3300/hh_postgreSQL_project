import psycopg2
from src.utils import get_env_variable

def create_database_and_tables():
    """
    Создаёт базу данных и таблицы employers и vacancies.
    """
    db_name = get_env_variable("DB_NAME")
    user = get_env_variable("DB_USER")
    password = get_env_variable("DB_PASSWORD")
    host = get_env_variable("DB_HOST") or "localhost"
    port = get_env_variable("DB_PORT")
    print("DEBUG db params (repr):")
    print("dbname=", repr(db_name))
    print("user=", repr(user))
    print("password=", repr(password))
    print("host=", repr(host))
    print("port=", repr(port))
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=int(port))
    conn.set_client_encoding('UTF8')
    conn.autocommit = True
    cur = conn.cursor()

    # Создание БД
    cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    conn.close()

    # Создание таблиц
    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
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
    cur.close()
    conn.close()
