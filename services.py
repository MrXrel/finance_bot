import re
from datetime import date
from db import DataBase
from exceptions import *


def add_expense_to_db(user_id: int, raw_message: str) -> tuple:
    """Parse message, add raw in db and return info about category and money spent on it"""
    pattern = re.compile(r'(.+) (\d+)')
    match = pattern.search(raw_message.lower())
    # if not found return False
    if not match:
        raise BadMessage
    category = match.group(1)

    # here is params
    money = match.group(2)
    category_name = check_the_category(category)
    db = DataBase('db.db')

    # if there isn't user table: create new table
    if not db.check_if_the_user_in_db(user_id):
        db.create_user_table(user_id)

    # add expense to the table
    db.add_expense(user_id, category_name, money, date.today())
    return category_name, money


def show_month_expense(user_id: int) -> str:
    """Show month expense"""
    db = DataBase('db.db')

    # get all expenses as a dict
    result = db.get_month_expenses(user_id)
    if not result:
        raise NoInformationException
    # get total sum of all expenses
    total = sum(result.values())

    # sort dict by money spent on category and get sorted list of tuples (category, money)
    result = sorted(result.items(), key=lambda item: item[1], reverse=True)

    # convert every tuple to string
    result = [f'{el[0].capitalize()}: {el[1]} руб.' for el in result]
    # make final message of all expences and return it
    final_message = '\n'.join(result) + f'\n*Всего*: {total} руб.'

    return final_message


def show_daily_expense(user_id: int) -> str:
    """Show daily expense"""
    db = DataBase('db.db')

    # get all expenses as a dict
    result = db.get_daily_expenses(user_id)
    if not result:
        raise NoInformationException
    # get total sum of all expenses
    total = sum(result.values())

    # sort dict by money spent on category and get sorted list of tuples (category, money)
    result = sorted(result.items(), key=lambda item: item[1], reverse=True)

    # convert every tuple to string
    result = [f'{el[0].capitalize()}: {el[1]} руб.' for el in result]
    # make final message of all expences and return it
    final_message = '\n'.join(result) + f'\n*Всего*: {total} руб.'

    return final_message


def delete_expense(user_id: int) -> tuple:
    """Delete expense and return info about deleted row"""
    # type error
    db = DataBase('db.db')
    # get deleted row
    deleted_row = db.del_last_expense(user_id)
    return deleted_row


def check_the_category(category_name) -> str:
    available_categories = ['продукты', 'коммунальные услуги', 'такси', 'кофе', 'транспорт', 'обслуживание машины',
                            'здоровье', 'кредит', 'книги', 'связь', 'покупка техники', 'интернет', 'подписки', 'кафе',
                            'прочее']
    # check the category name, if it is not found add to category others
    if category_name not in available_categories:
        category_name = 'прочее'

    return category_name


if __name__ == '__main__':
    check_the_category('такси')
