import psycopg2
from typing import List, Tuple, Optional
from src.utils import get_env_variable

class DBManager:
    """
    Класс для работы с базой данных hh_project.
    """
    def __init__(self):
        self.db_name = get_env_variable("DB_NAME")
        self.user = get_env_variable("DB_USER")
        self.password = get_env_variable("DB_PASSWORD")
        self.host = get_env_variable("DB_HOST") or "localhost"
        self.port = get_env_variable("DB_PORT")
        self.conn = psycopg2.connect(
            dbname=self.db_name, user=self.user, password=self.password, host=self.host, port=self.port
        )
        self.cur = self.conn.cursor()

    def insert_employer(self, employer_id: int, name: str, url: Optional[str]):
        """Вставка работодателя."""
        self.cur.execute(
            "INSERT INTO employers (employer_id, name, url) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
            (employer_id, name, url)
        )
        self.conn.commit()

    def insert_vacancy(self, vacancy_id: int, employer_id: int, title: str, salary_from: Optional[int],
                       salary_to: Optional[int], url: Optional[str]):
        """Вставка вакансии."""
        self.cur.execute(
            """INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, url)
               VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;""",
            (vacancy_id, employer_id, title, salary_from, salary_to, url)
        )
        self.conn.commit()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        self.cur.execute("""
            SELECT e.name, COUNT(v.vacancy_id)
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name;
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        self.cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id;
        """)
        return self.cur.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        self.cur.execute("""
            SELECT AVG((salary_from + salary_to)/2.0)
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
        """)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        avg = self.get_avg_salary()
        self.cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE (salary_from + salary_to)/2.0 > %s;
        """, (avg,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        self.cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE LOWER(v.title) LIKE %s;
        """, (f"%{keyword.lower()}%",))
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
