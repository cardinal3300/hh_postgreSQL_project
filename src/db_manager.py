from typing import Dict, List, Optional

import psycopg2

from src.utils import get_env_variable


class DBManager:
    """
        Класс для работы с базой данных hh_postgresql_project.
        Методы класса позволяют:
        - получать список компаний и количество вакансий у каждой,
        - получать все вакансии с деталями,
        - получать среднюю зарплату,
        - получать вакансии с зарплатой выше средней,
        - искать вакансии по ключевым словам.
        """

    def __init__(self):
        """
            Инициализация подключения к базе данных.
            Args:
                db_name (str): имя базы данных
                user (str): пользователь базы данных
                password (str): пароль пользователя
                host (str): хост базы данных (по умолчанию "localhost")
                port (int): порт базы данных (по умолчанию 5432)
            """

        self.db_name = get_env_variable("DB_NAME")
        self.user = get_env_variable("DB_USER")
        self.password = get_env_variable("DB_PASSWORD")
        self.host = get_env_variable("DB_HOST")
        self.port = get_env_variable("DB_PORT")

        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor()


    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """
            Получает список всех компаний и количество вакансий у каждой компании.
            Returns:
                List[Dict]: список словарей с полями 'company' и 'vacancies_count'
            """

        self.cur.execute("""
            SELECT e.name, COUNT(v.vacancy_id) AS vacancies_count
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name
            ORDER BY vacancies_count DESC;
        """)

        return [{"company": r[0], "vacancies_count": r[1]} for r in self.cur.fetchall()]


    def get_all_vacancies(self) -> List[Dict]:
        """
            Получает список всех вакансий с указанием названия компании,
            названия вакансии, зарплаты и ссылки на вакансию.
            Returns:
                List[Dict]: список словарей с полями 'company', 'title', 'salary_from', 'salary_to', 'url'
            """

        self.cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id;
        """)
        return [
            {"company": r[0], "title": r[1], "salary_from": r[2], "salary_to": r[3], "url": r[4]}
            for r in self.cur.fetchall()
        ]


    def get_avg_salary(self) -> Optional[float]:
        """
            Получает среднюю зарплату по вакансиям.
            Returns:
                float: средняя зарплата по всем вакансиям (среднее значение salary_from и salary_to)
            """

        self.cur.execute("""
            SELECT AVG((salary_from + salary_to)/2.0)
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
        """)
        avg = self.cur.fetchone()[0]
        return float(avg) if avg is not None else None


    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """
            Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
            Returns:
                List[Dict]: список словарей с полями 'company', 'title', 'salary_from', 'salary_to', 'url'
            """

        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []

        self.cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE ((v.salary_from + v.salary_to)/2.0) > %s;
        """, (avg_salary,))
        return [
            {"company": r[0], "title": r[1], "salary_from": r[2], "salary_to": r[3], "url": r[4]}
            for r in self.cur.fetchall()
        ]


    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """
            Получает список всех вакансий, в названии которых содержится переданное слово.
            Args:
                keyword (str): ключевое слово для поиска в названии вакансии
            Returns:
                List[Dict]: список словарей с полями 'company', 'title', 'salary_from', 'salary_to', 'url'
            """

        self.cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE v.title ILIKE %s;
        """,(f"%{keyword}%",))
        return [
            {"company": r[0], "title": r[1], "salary_from": r[2], "salary_to": r[3], "url": r[4]}
            for r in self.cur.fetchall()
        ]


    def close(self):
        """Закрывает соединение с базой данных."""
        self.cur.close()
        self.conn.close()
