import psycopg2
from psycopg2.extensions import connection, cursor

class DBManager:
    """
    Класс для работы с базой данных hh_postgresql_project.
    """
    conn: connection
    cur: cursor

    def __init__(self, db_name, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()


    def execute(self, query: str, params: tuple = None):
        """Выполнение запроса к базе данных."""
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            try:
                return cur.fetchall()
            except psycopg2.ProgrammingError:
                return None

    def insert_employer(self, employer_id, name, url):
        self.cur.execute(
            """
            INSERT INTO employers (employer_id, name, url)
            VALUES (%s, %s, %s) ON CONFLICT (employer_id) DO NOTHING;
            """,
            (employer_id, name, url)
        )
        self.conn.commit()

    def insert_vacancy(self, vacancy_id, employer_id, title, salary_from, salary_to, url):
        self.cur.execute(
            """
            INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, url)
            VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (vacancy_id) DO NOTHING;
            """,
            (vacancy_id, employer_id, title, salary_from, salary_to, url)
        )
        self.conn.commit()


    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.vacancy_id)
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name;
            """)
            return cur.fetchall()


    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id;
            """)
            return cur.fetchall()


    def get_avg_salary(self):
        """
        Получает среднюю зарплату по всем вакансиям.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to)/2.0)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            """)
            return cur.fetchone()[0]


    def get_vacancies_with_higher_salary(self):
        """
        Получает список вакансий, у которых зарплата выше средней.
        """
        avg = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE (v.salary_from + v.salary_to)/2.0 > %s;
            """, (avg,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список вакансий, в названии которых содержится ключевое слово.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.title LIKE %s;
            """, (f"%{keyword}%",))
            return cur.fetchall()


    def close(self):
        """Закрытие подключения."""
        self.cur.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
