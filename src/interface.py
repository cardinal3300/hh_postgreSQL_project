from src.db_manager import DBManager

def user_interface(db: DBManager):
    """Простой текстовый интерфейс для пользователя."""
    print("Компании и количество вакансий:")
    for name, count in db.get_companies_and_vacancies_count():
        print(f"{name}: {count} вакансий")

    print("\nВсе вакансии:")
    for name, title, sal_from, sal_to, url in db.get_all_vacancies():
        salary = f"{sal_from}-{sal_to}" if sal_from and sal_to else "Не указана"
        print(f"{name} | {title} | {salary} | {url}")

    print("\nСредняя зарплата по вакансиям:")
    print(db.get_avg_salary() or "Нет данных")

    print("\nВакансии с зарплатой выше средней:")
    for name, title, sal_from, sal_to, url in db.get_vacancies_with_higher_salary():
        salary = f"{sal_from}-{sal_to}" if sal_from and sal_to else "Не указана"
        print(f"{name} | {title} | {salary} | {url}")

    keyword = input("\nВведите ключевое слово для поиска вакансий: ")
    print(f"\nВакансии с ключевым словом '{keyword}':")
    for name, title, sal_from, sal_to, url in db.get_vacancies_with_keyword(keyword):
        salary = f"{sal_from}-{sal_to}" if sal_from and sal_to else "Не указана"
        print(f"{name} | {title} | {salary} | {url}")
