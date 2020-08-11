from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.callback_data import CallbackData

data = CallbackData('content', 'action', 'button_name')


def all_buttons():
    all_buttons = InlineKeyboardMarkup(row_width=3)
    utility_button = InlineKeyboardButton(
        'Utility', callback_data=data.new(action='Utility', button_name='-'))
    add_category_button = InlineKeyboardButton(
        'Add category', callback_data=data.new(action='add_category',
                                               button_name='-'))
    add_expense_button = InlineKeyboardButton(
        'Add expence', callback_data=data.new(action='add_expense',
                                              button_name='-'))

    all_buttons.add(add_category_button, add_expense_button)
    drop = InlineKeyboardButton(
        'Drop', callback_data=data.new(action='drop', button_name='-'))

    all_buttons.add(drop, utility_button)

    return all_buttons


def utility_buttons():
    utils_buttons = InlineKeyboardMarkup(row_width=3)
    day_expenses_button = InlineKeyboardButton(
        'My day expenses', callback_data=data.new(action='get_day_expenses',
                                                  button_name='-'))
    categories_button = InlineKeyboardButton(
        'Show categories', callback_data=data.new(action='show_categories',
                                                  button_name='-'))
    report_button = InlineKeyboardButton(
        'Get report', callback_data=data.new(action='get_report',
                                             button_name='-'))
    balance_button = InlineKeyboardButton(
        'Get balance', callback_data=data.new(action='get_balance',
                                              button_name='-'))
    back_button = InlineKeyboardButton(
        'Back', callback_data=data.new(action='back_to_main', button_name='-'))

    utils_buttons.add(day_expenses_button, categories_button)
    utils_buttons.add(report_button)
    utils_buttons.add(balance_button)
    utils_buttons.add(back_button)

    return utils_buttons


def drop_buttons():
    drop_categories = InlineKeyboardButton(
        'Drop categories', callback_data=data.new(action='drop_category',
                                                  button_name='-'))
    drop_expense = InlineKeyboardButton(
        'Drop expenses', callback_data=data.new(action='drop_expenses',
                                                button_name='-'))
    back_button = InlineKeyboardButton(
        'Back', callback_data=data.new(action='back_to_main', button_name='-'))
    drop = InlineKeyboardMarkup(row_width=2).add(drop_categories, drop_expense)
    drop.add(back_button)
    return drop


def delete_category(categories_list=None):
    categories = InlineKeyboardMarkup(row_width=2)
    for category in categories_list:
        if category != 'Баланс':
            buton1 = InlineKeyboardButton(
                str(category), callback_data=data.new(action='delete',
                                                      button_name=str(category)
                                                      ))
            categories.add(buton1)
    back_button = InlineKeyboardButton(
        'Back', callback_data=data.new(action='back_to_main',
                                       button_name='back'))
    categories.add(back_button)
    return categories


def only_back_button():
    back_button = InlineKeyboardMarkup(row_width=2)
    button = InlineKeyboardButton(
        'Back', callback_data=data.new(action='back_to_main',
                                       button_name='back'))
    back_button.add(button)
    return back_button


def choose_category_expense(categories_list=None):
    # print()
    categories = InlineKeyboardMarkup(row_width=2)
    balance_button_name = categories_list.pop(categories_list.index('Баланс'))
    balance_button = InlineKeyboardButton(
        balance_button_name, callback_data=data.new(action='balance',
                                                    button_name='-'))
    categories.add(balance_button)
    for category in categories_list:
        category_button = InlineKeyboardButton(
            str(category), callback_data=data.new(action='choose',
                                                  button_name=str(category)))
        categories.add(category_button)
    back_button = InlineKeyboardButton(
        'Back', callback_data=data.new(action='back_to_main',
                                       button_name='back'))
    categories.add(back_button)
    return categories


def last_five(last_expenses=None):
    expenses = InlineKeyboardMarkup(row_width=2)
    for expense in last_expenses:
        last_expense = last_expenses[expense]
        button_title = last_expense['category'] + ' ' + \
                       last_expense['merchandise'] + ' ' + \
                       str(last_expense['price'])
        button = InlineKeyboardButton(button_title,
                                      callback_data=data.new(
                                          action='choose_and_delete',
                                          button_name=str(
                                              last_expense['expense_id'])))
        expenses.add(button)
    back_button = InlineKeyboardButton(
        'Back', callback_data=data.new(action='back_to_main',
                                       button_name='back'))
    expenses.add(back_button)
    return expenses

# res = ReplyKeyboardRemove()

# при нажатии кнопки поменять состояние
