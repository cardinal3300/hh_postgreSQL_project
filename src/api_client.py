from typing import List, Dict
import requests

BASE_URL = "https://api.hh.ru"

EMPLOYERS_LIST = [
    {"id": 1740, "name": "Яндекс"},
    {"id": 3529, "name": "СБЕР"},
    {"id": 78638, "name": "Т-Банк"},
    {"id": 15478, "name": "VK"},
    {"id": 2180, "name": "Ozon"},
    {"id": 4219, "name": "Т2"},
    {"id": 3776, "name": "МТС"},
    {"id": 80, "name": "Альфа-Банк"},
    {"id": 3127, "name": "Мегафон"},
    {"id": 2748, "name": "Ростелеком"}
]

def get_employer_info(employer_id: int) -> Dict:
    """Получает данные о работодателе по employer_id."""
    response = requests.get(f"{BASE_URL}/employers/{employer_id}")
    if response.status_code != 200:
        print(f"[WARN] Работодатель {employer_id} не найден, статус {response.status_code}")
        return {}
    return response.json()


def get_employers_data() -> List[Dict]:
    """Возвращает данные о 10 работодателях."""
    employers = []
    for emp in EMPLOYERS_LIST:
        data = get_employer_info(emp["id"])
        if not data:
            continue
        name = data.get("name")
        url = data.get("alternate_url")
        employers.append({
            "id": data.get("id"),
            "name": name,
            "url": url
        })
    return employers


def get_vacancies(employer_id: int, per_page: int = 100) -> List[Dict]:
    """Получает вакансии работодателя по employer_id."""
    vacancies = []
    page = 0
    while True:
        params = {"employer_id": employer_id, "per_page": per_page, "page": page}
        response = requests.get(f"{BASE_URL}/vacancies", params=params)
        if response.status_code != 200:
            print(f"[WARN] Не удалось получить вакансии для {employer_id}, статус {response.status_code}")
            return []
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
        emp_id = emp.get("id")
        if not emp_id:
            continue

        vacs = get_vacancies(emp_id)

        for vac in vacs:
            if "id" not in vac or "employer" not in vac:
                continue
            all_vacancies.append(vac)
    return all_vacancies
