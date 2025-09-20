from src.db_setup import create_database_and_tables
from src.api_client import get_employers_data, get_vacancies_data
from src.loader import load_employers, load_vacancies
from src.db_manager import DBManager
from src.interface import user_interface
from src.utils import get_env_variable

def main():
    print("Создание базы данных и таблиц...")
    create_database_and_tables()

    print("Получение данных о компаниях...")
    employers = get_employers_data()

    print("Получение вакансий компаний...")
    vacancies = get_vacancies_data(employers)

    db = DBManager(
        db_name=get_env_variable("DB_NAME"),
        user=get_env_variable("DB_USER"),
        password=get_env_variable("DB_PASSWORD"),
        host=get_env_variable("DB_HOST"),
        port=get_env_variable("DB_PORT"),
    )

    print("Заполнение таблицы работодателей...")
    load_employers(db, employers)

    print("Заполнение таблицы вакансий...")
    load_vacancies(db, vacancies)

    print("\nЗапуск интерфейса пользователя...")
    user_interface(db)

    db.close()
    print("\nРабота завершена.")


if __name__ == "__main__":
    main()