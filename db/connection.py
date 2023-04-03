import mysql.connector
from datetime import datetime, timedelta
from config import *

class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Connection Error')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Singleton
class DBConnector(object):
    def __init__(self):
        self.create_connection()

    def __str__(self):
        return 'Database connection object'

    def create_connection(self):
        self.conn = mysql.connector.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=DATABASE
        )

        self.curr = self.conn.cursor()

    def store_db(self, item):
        self.curr.execute(
            "select * from  where source_id = %s and website = %s", 
            (item['source_id'], item['website'])
        )
        result = self.curr.fetchone()

        self.curr.execute('INSERT INTO vacancies.indeed_job '\
                        ' (source_id, position, company, location, salary, schedule, education, work_experience, phone, email, short_description, full_description, link, website, logo, created_at)'\
                        ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(
                            is_not_null(item['source_id']),
                            is_not_null(item['position']),
                            is_not_null(item['company']),
                            is_not_null(item['location']),
                            is_not_null(item['salary']),
                            is_not_null(item['schedule']),
                            is_not_null(item['education']),
                            is_not_null(item['work_experience']),
                            is_not_null(item['phone']),
                            is_not_null(item['email']),
                            # is_not_null(item['shift']),
                            is_not_null(item['short_description'][0:255]),
                            is_not_null(item['full_description'][0:1000]),
                            is_not_null(item['link']),
                            is_not_null(item['website']),
                            is_not_null(item['logo_url']),
                            datetime.now()))
    
        self.conn.commit()

    def get_all_compaies(self) -> list[tuple]:
        self.curr.execute(
            "select Company from JOBS_FINDER.verified_companies", 
        )

        companies = self.curr.fetchall()
        companies = list(map(lambda s: s[0],companies))
        companies = list(filter(lambda s: s != '',companies))

        return companies

def is_not_null(item):
    return '' if item is None else str(item).strip()