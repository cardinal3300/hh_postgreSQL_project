from src.db_manager import DBManager


def user_interface(db: DBManager):
    """
    Простой текстовый интерфейс для взаимодействия с пользователем.
    Пользователь может выбрать действия и увидеть результаты работы методов DBManager.
    """

    while True:
        print("\n=== Меню пользователя ===")
        print("1. Список компаний и количество вакансий")
        print("2. Список всех вакансий")
        print("3. Средняя зарплата по вакансиям")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            companies = db.get_companies_and_vacancies_count()
            print("\nКомпании и количество вакансий:")
            for name, count in companies:
                print(f"- {name}: {count} вакансий")

        elif choice == "2":
            vacancies = db.get_all_vacancies()
            print("\nВсе вакансии:")
            for vac in vacancies:
                name, title, salary, url = vac
                print(f"- {name}: {title}, зарплата: {salary}, ссылка: {url}")

        elif choice == "3":
            avg_salary = db.get_avg_salary()
            print(f"\nСредняя зарплата по вакансиям: {avg_salary}")

        elif choice == "4":
            high_salary_vacancies = db.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше средней:")
            for vac in high_salary_vacancies:
                name, title, salary, url = vac
                print(f"- {name}: {title}, зарплата: {salary}, ссылка: {url}")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска вакансий: ").strip()
            vacancies = db.get_vacancies_with_keyword(keyword)
            print(f"\nВакансии с ключевым словом '{keyword}':")
            for vac in vacancies:
                name, title, salary, url = vac
                print(f"- {name}: {title}, зарплата: {salary}, ссылка: {url}")

        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")
