from src.db_setup import create_database_and_tables
from src.api_client import get_employers_data, get_vacancies_data
from src.loader import load_employers, load_vacancies
from src.db_manager import DBManager
from src.interface import user_interface

def main():
    print("Создание базы данных и таблиц...")
    create_database_and_tables()

    print("Получение данных о компаниях...")
    employers = get_employers_data()

    print("Получение вакансий компаний...")
    vacancies = get_vacancies_data(employers)

    db = DBManager()  # создаём один экземпляр для работы с БД

    print("Заполнение таблицы работодателей...")
    load_employers(db, employers)

    print("Заполнение таблицы вакансий...")
    load_vacancies(db, vacancies)
    print(f"Всего добавлено вакансий: {len(vacancies)}")

    # Демонстрация поиска по ключевому слову
    keyword = input("Введите ключевое слово для поиска вакансий: ").strip()
    found_vacancies = db.get_vacancies_with_keyword(keyword)
    print(f"Найдено вакансий с ключевым словом '{keyword}': {len(found_vacancies)}")

    print("\nЗапуск интерфейса пользователя...")
    user_interface(db)
    db.close()
    print("\nРабота завершена.")


if __name__ == "__main__":
    main()
