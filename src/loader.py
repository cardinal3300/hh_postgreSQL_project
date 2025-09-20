from typing import List, Dict
from src.db_manager import DBManager

def load_employers(db: DBManager, employers: List[Dict]):
    """Заполняет таблицу employers."""
    for emp in employers:
        db.insert_employer(emp["id"], emp["name"], emp.get("url"))

def load_vacancies(db: DBManager, vacancies: List[Dict]):
    """Заполняет таблицу vacancies."""
    for vac in vacancies:
        salary = vac.get("salary") or {}
        db.insert_vacancy(
            vac["id"],
            vac["employer"]["id"],
            vac["title"],
            salary.get("salary_from"),
            salary.get("salary_to"),
            vac.get("url")
        )
