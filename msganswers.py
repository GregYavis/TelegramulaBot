import random
import message_parser
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

category_exists = 'Данная категория уже существует'
user_hasnt_categoty = 'Вы ещё не создали ни одной категории\n' \
                      'Создайте категорию сипользуя ввод /add "Имя_категории"'
bot_commandslist = 'Список доступных комманд:\n' \
                   '/help - Вывод справочной информации\n' \
                   '/start - Приветствие\n' \
                   '/add "Имя_категории" - добавить свою категорию\n' \
                   '/dreport - Отчёт за текущий день\n' \
                   '/categories - Список пользовательских категорий\n'

start = 'На данный момент функционал бота находится в разработке'
expense_added = "Занесено в базу данных"

async def manual_text(user_firstname):
    manual = 'Привет {0}.\n\n' \
             'Этот бот позволяет вести учёт собственных финансов.\n' \
             'Добавить собственную категорию можно ' \
             'воспользовавшись вводом:\n' \
             '/add "Имя_категории"\n' \
             'Посмотреть список своих категорий:\n' \
             '/categories\n' \
             'Вывести отчёт за сегодняшний день:\n' \
             '/dreport\n' \
             'Используй следущий синтаксис для занесения новых данных:\n' \
             '<категория> <название товара/услуги> <цена>\n' \
             'Например:\n' \
             'Макдональдс маккомбо 225р\n' \
             'Cписок команд:\n' \
             '/commandslist'.format(user_firstname)
    return manual

async def add_category_answers(*ret):
    answer = ret
    if answer[0] is False:
        answer_massage = "collection dosn't exist"
        return answer_massage
    elif answer[1]:
        answer_massage = "category already exists"
        return answer_massage
    else:
        answer_massage = "its okay to by GAY"
        return answer_massage

async def add_expence_answers(*flags, category, text):
    flags = flags
    if flags[0] is False:
        answer_massage = 'Категории не существует\n' \
                         'Вы можете создать её командой\n' \
                         '/add {0}'.format(category.capitalize())
        return answer_massage
    elif flags[1] is False:
        answer_massage = Price_not_found(text)
        return answer_massage
    else:
        answer_massage = "Занесено в базу данных"
        return answer_massage


def rand_price():
    return random.randrange(150, 1000, 150)


def Price_not_found(text):
    price_not_found = 'К сожалению я не вижу что бы вы указали цену\n' \
                      'или возможно указали её не последней в строке.\n' \
                      'Попробуйте, например ввести:\n{0} {1}р'.format(
        str(text).capitalize(),
        rand_price())
    return price_not_found
