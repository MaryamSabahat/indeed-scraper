import mysql.connector
from datetime import datetime
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
        )

        self.curr = self.conn.cursor()

    def store_db(self, item: dict):        
        self.curr.execute('INSERT INTO vacancies.reviews '\
                        ' (company, reviews_amount, work_life_rate, pay_benefits_rate, security_adv_rate, management_rate, culture_rate, reviewer_rate, caption, reviewer_position, reviewer_location, date_reviewed, text, date_added)'\
                        ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(
                            is_not_null(item['company']),
                            is_not_null(item['reviews_amount']),
                            is_not_null(item['work_life_rate']),
                            is_not_null(item['pay_benefits_rate']),
                            is_not_null(item['security_adv_rate']),
                            is_not_null(item['management_rate']),
                            is_not_null(item['culture_rate']),
                            is_not_null(item['reviewer_rate']),
                            is_not_null(item['caption']),
                            is_not_null(item['reviewer_position']),
                            is_not_null(item['reviewer_location']),
                            is_not_null(item['date_reviewed']),
                            is_not_null(item['text']),
                            datetime.now())
        )
    
        self.conn.commit()

    def get_all_compaies(self) -> list[tuple]:
        self.curr.execute(
            "select Company from JOBS_FINDER.verified_companies", 
        )

        companies = self.curr.fetchall()
        companies = map(lambda s: s[0],companies)
        companies = list(filter(lambda s: s != '',companies))

        return companies

def is_not_null(item):
    return '' if item is None else str(item).strip()