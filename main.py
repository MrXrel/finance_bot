import logging
from services import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '1796514848:AAGJd3MwGg50E8EUl3sT34O7SgAuEGw-yEE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Gives basic information and commands
    """
    me = await bot.get_me()
    await message.answer(
        f"Привет ***{message.from_user.first_name}***!\nЯ *{me.first_name}* бот учета финансов.\nСписок команд можно увидеть написав команду /help.",
        parse_mode='Markdown')


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    """
    Gives commands how to work with bot
    """
    await message.answer(
        "Чтобы записать трату напишите сообщение, например: такси 100. Пишите согласно категориям, если категория не распознана, то расход добавляется в прочее. Подробнее в /categories.\n"
        "Чтобы посмотерть расходы за месяц напишите _/month_.\n"
        "Чтобы посмотерть расходы за день напишите _/day_.", parse_mode='Markdown')


@dp.message_handler(commands=['categories'])
async def send_categories(message: types.Message):
    """
    Gives all categories names
    """
    categories = ['- продукты', '- коммунальные услуги', '- такси', '- кофе', '- транспорт', '- обслуживание машины',
                  '- здоровье', '- кредит', '- книги', '- связь', '- покупка техники', '- интернет', '- подписки',
                  '- кафе', '- прочее']

    await message.answer('Доступные категории:\n' + '\n'.join(categories), parse_mode='Markdown')


@dp.message_handler(commands=['month'])
async def get_month_expenses(message: types.Message):
    """Show user his month expanses on every category"""
    try:
        message_text = show_month_expense(message.from_user.id)
        await message.answer(message_text, parse_mode='Markdown')
    except UserNotFound:
        await message.answer('Извините, но вы еще не делали никаких записей.')
    except NoInformationException:
        await message.answer('У вас нет расходов за этот месяц.')


@dp.message_handler(commands=['day'])
async def get_month_expenses(message: types.Message):
    """Show user his today expanses on every category"""
    try:
        message_text = show_month_expense(message.from_user.id)
        await message.answer(message_text, parse_mode='Markdown')
    except UserNotFound:
        await message.answer('Извините, но вы еще не делали никаких записей.')
    except NoInformationException:
        await message.answer('У вас нет расходов за этот день.')


@dp.message_handler(commands=['dellast'])
async def delete_last_expense(message: types.Message):
    """Delete last row in db and say user info about deleted row"""
    try:
        deleted_row = delete_expense(message.from_user.id)
        await message.answer(f'Удалил расход {deleted_row[1]} за {deleted_row[2]} рублей от {deleted_row[3]}')
    except TypeError:
        await message.answer('У вас нет записей расходов.')
    except UserNotFound:
        await message.answer('Вы еще не записывали свои расходы.')


@dp.message_handler(regexp=r'/.*')
async def filter_bad_commands(message: types.Message):
    """Catch bad commands"""
    await message.answer('Я не знаю таких комманд.')


@dp.message_handler(content_types=['text'])
async def get_the_text(message: types.Message):
    """Get the user text and parse it. if it isn't correct it will say it user"""
    user_text = message.text
    try:
        result = add_expense_to_db(message.from_user.id, user_text)
        await message.answer(f'Ваш расход был записан в категорию *{result[0]}* за *{result[1]} рублей*.',
                             parse_mode='Markdown')
    except BadMessage:
        # if message wrote in wrong format
        await message.answer('Вы написали трату в неправильном формате!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
