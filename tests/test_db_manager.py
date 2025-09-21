import pytest
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
    """Фикстура для подключения к базе данных"""
    manager = DBManager(**DB_PARAMS)
    yield manager
    manager.close()

def test_get_avg_salary(db):
    avg_salary = db.get_avg_salary()
    assert avg_salary is None or isinstance(avg_salary, float), "Средняя зарплата должна быть float или None"

def test_get_companies_and_vacancies_count(db):
    companies = db.get_companies_and_vacancies_count()
    assert isinstance(companies, list), "Метод должен возвращать список"
    if companies:
        assert "company" in companies[0] and "vacancies_count" in companies[0]

def test_get_vacancies_with_keyword(db):
    keyword = "python"
    vacancies = db.get_vacancies_with_keyword(keyword)
    assert isinstance(vacancies, list)
    for vac in vacancies:
        assert keyword.lower() in vac["title"].lower()
