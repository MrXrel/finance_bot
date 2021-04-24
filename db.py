import sqlite3 as sql

from datetime import date
from dateutil.relativedelta import relativedelta

from exceptions import *


class DataBase:
    def __init__(self, database: str):
        """Initializing connection with database and getting cursor"""
        self.con = sql.connect(database)
        self.cur = self.con.cursor()

    def check_if_the_user_in_db(self, user_id: int) -> bool:
        """Check if person in db and return True of False"""
        self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='U{user_id}'")
        result = self.cur.fetchall()
        if len(result) == 0:
            return False
        else:
            return True

    def create_user_table(self, user_id: int):
        """Create new table in db"""
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS U{user_id}("
                         "id integer PRIMARY KEY,"
                         "where_spent text,"
                         "how_much_spent integer,"
                         "date_spent date)")

    def get_all_expenses(self, user_id: int):
        self.cur.execute(f"SELECT * FROM U{user_id}")
        result = self.cur.fetchall()
        return result

    def get_month_expenses(self, user_id: int) -> dict:
        """Get month expenses from db and return dict"""
        # check if the user in db and raise exception
        if not self.check_if_the_user_in_db(user_id):
            raise UserNotFound

        month_ago_date = date.today() - relativedelta(months=1) - relativedelta(days=1)
        self.cur.execute(f"SELECT * FROM U{user_id} WHERE date_spent > '{month_ago_date}' ORDER BY where_spent")
        result = self.cur.fetchall()
        # count how much was spend per month
        sum_of_categories = self._count_sum_of_categories(result)
        return sum_of_categories

    def get_daily_expenses(self, user_id: int) -> dict:
        """Get daily expenses from db and return dict"""
        # check if the user in db and raise exception
        if not self.check_if_the_user_in_db(user_id):
            raise UserNotFound

        today_date = date.today() - relativedelta(days=1)
        self.cur.execute(f"SELECT * FROM U{user_id} WHERE date_spent > '{today_date}' ORDER BY where_spent")
        result = self.cur.fetchall()
        # count how much was spend per month
        sum_of_categories = self._count_sum_of_categories(result)

        return sum_of_categories

    def add_expense(self, user_id: int, where_spent: str, how_much_spent: int, date_spent: str):
        self.cur.execute(f"INSERT INTO U{user_id}(where_spent, how_much_spent, date_spent) VALUES(?,?,?)",
                         (where_spent, how_much_spent, date_spent))
        self.con.commit()

    def del_last_expense(self, user_id: int) -> tuple:
        """Delete last expense from the table and return info about this expense"""
        # TODO Make exception when table is empty
        # check if the user in db and raise exception
        if not self.check_if_the_user_in_db(user_id):
            raise UserNotFound
        last_id = self.cur.execute(f"SELECT * FROM U{user_id} ORDER BY id DESC LIMIT 1").fetchone()[0]
        deleted_row = self.cur.execute(f"SELECT * FROM U{user_id} WHERE id={last_id}").fetchone()
        self.cur.execute(f"DELETE FROM U{user_id} WHERE id={last_id}")
        self.con.commit()
        return deleted_row

    def _count_sum_of_categories(self, list_of_categories: list) -> dict:
        """Get sorted dict with expenses. Then sum expenses for every category"""
        result = {}
        current_category_name = ''
        for category in list_of_categories:
            if current_category_name != category[1]:
                current_category_name = category[1]
                # sum money in every category
                result[current_category_name] = 0
            result[current_category_name] += category[2]
        return result


if __name__ == '__main__':
    db = DataBase('db.db')
    # db.add_expense(779522522, 'продукты', 800, '2021-04-23')
    print(db.del_last_expense(779522522))
