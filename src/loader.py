from typing import List, Dict
from src.db_manager import DBManager

def load_employers(employers: List[Dict]):
    """Заполняет таблицу employers."""
    db = DBManager()
    for emp in employers:
        db.insert_employer(emp["id"], emp["name"], emp.get("alternate_url"))
    db.close()

def load_vacancies(vacancies: List[Dict]):
    """Заполняет таблицу vacancies."""
    db = DBManager()
    for vac in vacancies:
        salary = vac.get("salary") or {}
        db.insert_vacancy(
            vac["id"],
            vac["employer"]["id"],
            vac["name"],
            salary.get("from"),
            salary.get("to"),
            vac.get("alternate_url")
        )
    db.close()
