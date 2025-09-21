from typing import Dict, List

from src.db_manager import DBManager


def load_employers(db: DBManager, employers: List[Dict]):
    """
    Заполняет таблицу employers.
    Args:
        db (DBManager): экземпляр класса DBManager.
        employers (List[Dict]): список словарей с информацией о работодателях.
    """
    inserted_count = 0
    for emp in employers:
        try:
            db.cur.execute(
                "INSERT INTO employers (employer_id, name, url) VALUES (%s, %s, %s) "
                "ON CONFLICT (employer_id) DO NOTHING;",
                (emp["id"], emp["name"], emp.get("alternate_url"))
            )
            inserted_count += 1
        except Exception as e:
            print(f"Ошибка при добавлении работодателя {emp.get('name')}: {e}")
    db.conn.commit()
    print(f"Добавлено работодателей: {inserted_count}")


def load_vacancies(db: DBManager, vacancies: List[Dict]):
    """
    Заполняет таблицу vacancies.
    Args:
        db (DBManager): экземпляр класса DBManager.
        vacancies (List[Dict]): список словарей с информацией о вакансиях.
    """
    inserted_count = 0
    for vac in vacancies:
        salary = vac.get("salary") or {}
        try:
            db.cur.execute(
                "INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, url) "
                "VALUES (%s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (vacancy_id) DO NOTHING;",
                (
                    vac["id"],
                    vac["employer"]["id"],
                    vac["name"],
                    salary.get("from"),
                    salary.get("to"),
                    vac.get("alternate_url")
                )
            )
            inserted_count += 1
        except Exception as e:
            print(f"Ошибка при добавлении вакансии {vac.get('name')}: {e}")
    db.conn.commit()
    print(f"Добавлено вакансий: {inserted_count}")
