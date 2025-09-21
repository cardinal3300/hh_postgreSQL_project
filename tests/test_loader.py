import pytest
from src.loader import load_employers, load_vacancies
from src.db_manager import DBManager

DB_PARAMS = {
    "db_name": "hh_postgresql_project",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}

@pytest.fixture

def db():
    manager = DBManager(**DB_PARAMS)
    yield manager
    manager.close()

def test_load_employers(db):
    employers = [
        {"employer_id": 9999, "name": "TestCorp", "url": None}
    ]
    load_employers(db, employers)
    companies = db.get_companies_and_vacancies_count()
    assert any(c["company"] == "TestCorp" for c in companies)

def test_load_vacancies(db):
    vacancies = [
        {"vacancy_id": 9999, "employer_id": 9999, "title": "Test Engineer",
         "salary_from": 50000, "salary_to": 70000, "url": None}
    ]
    load_vacancies(db, vacancies)
    all_vacancies = db.get_all_vacancies()
    assert any(v["title"] == "Test Engineer" for v in all_vacancies)
