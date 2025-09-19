from typing import List, Dict
import requests

BASE_URL = "https://api.hh.ru"

EMPLOYERS_LIST = [
    {"id": 1740, "name": "Яндекс"},
    {"id": 1133, "name": "СберБанк"},
    {"id": 1577, "name": "Тинькофф"},
    {"id": 2456, "name": "VK"},
    {"id": 3345, "name": "Ozon"},
    {"id": 4423, "name": "Авито"},
    {"id": 5555, "name": "МТС"},
    {"id": 6231, "name": "Альфа-Банк"},
    {"id": 7123, "name": "Лаборатория Касперского"},
    {"id": 8099, "name": "Ростелеком"}
]

def get_employer_info(employer_id: int) -> Dict:
    """Получает данные о работодателе по employer_id."""
    response = requests.get(f"{BASE_URL}/employers/{employer_id}")
    return response.json()


def get_employers_data() -> List[Dict]:
    """Возвращает данные о 10 работодателях."""
    employers = []
    for emp in EMPLOYERS_LIST:
        data = get_employer_info(emp["id"])
        employers.append(data)
    return employers


def get_vacancies(employer_id: int, per_page: int = 100) -> List[Dict]:
    """Получает вакансии работодателя по employer_id."""
    vacancies = []
    page = 0
    while True:
        params = {"employer_id": employer_id, "per_page": per_page, "page": page}
        response = requests.get(f"{BASE_URL}/vacancies", params=params)
        data = response.json()
        vacancies.extend(data.get("items", []))
        if page >= data.get("pages", 0) - 1:
            break
        page += 1
    return vacancies


def get_vacancies_data(employers: List[Dict]) -> List[Dict]:
    """Возвращает вакансии для списка работодателей."""
    all_vacancies = []
    for emp in employers:
        emp_id = emp["id"]
        vacancies = get_vacancies(emp_id)
        all_vacancies.extend(vacancies)
    return all_vacancies
