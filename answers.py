import random

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
drop = 'Выберите что удалить'
drop_categories = 'Ваши категории позабыты'
drop_expenses = 'Ваши траты позабыты'
add_category = 'Введите название категории и отправьте мне'
category_added = 'Категория была добавлена'
please_choose_category = 'Выберите категорию'
category_exists_false = 'Вы ещё не создали ни одной категории'
cancel = 'Действие отменено'
input_number = 'Введите цифру'
day_expense_false = 'Сегодня вы ни на что не тратились'
report_false ='Вы ещё ни на что не тратились'
choose_category_to_delete = 'Выберите категорию для удаления'
expense_deleted = 'Запись удалена'
choose_expense_to_delete = 'Выбор траты для удаления'
expenses_exists_false = 'Ваши траты уже удалены либо ещё отсутствуют'
balance_exists_false = 'Вы не задали начальный баланс'
input_balance = 'Введите значение баланса'
invalid_input = 'Неверный формат'
invalid_update_input = 'Неверный формат обновления'
invalid_balance_input = 'Неверный формат баланса'
update_balance = 'Введите значение которое добавится к текущему балансу'
async def manual_text(user_firstname):
    manual = 'Привет {0}.\n\n' \
             'Этот бот позволяет вести учёт собственных финансов.\n' \
             'Добавить собственную категорию можно ' \
             'нажав кнопку, почле чего необходимо ввести имя\n' \
             'категории"\n' \
             'Вывести отчёт за сегодняшний день:\n' \
             '/dreport\n' \
             'Используй следущий синтаксис для занесения новых данных:\n' \
             '<категория>\n' \
             '<название товара/услуги>\n' \
             '<цена>\n' \
             'Или:\n' \
             '<категория> <название товара/услуги> <цена>\n' \
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
