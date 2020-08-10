from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData

data = CallbackData('content', 'action', 'button_name')


def all_buttons(cancel_button=False):
    categories_button = InlineKeyboardButton('Show my categories',
                                             callback_data=data.new(action=
                                                                    'show_categories',
                                                                    button_name='-'))
    add_category_button = InlineKeyboardButton('Add category',
                                               callback_data=data.new(action=
                                                                      'add_category',
                                                                      button_name='-'))
    add_expense_button = InlineKeyboardButton('Add expence',
                                              callback_data=data.new(action=
                                                                     'add_expense',
                                                                     button_name='-'))
    day_expenses_button = InlineKeyboardButton('My day expenses', callback_data=
                                               data.new(action =
                                                        'get_day_expenses',
                                                        button_name='-'))
    all_buttons = InlineKeyboardMarkup(row_width=3)
    all_buttons.add(add_category_button, add_expense_button)
    all_buttons.add(day_expenses_button)
    drop = InlineKeyboardButton('Drop', callback_data=data.new(action='drop',
                                                               button_name='-'))
    all_buttons.add(drop, categories_button)
    if cancel_button:
        cancel = InlineKeyboardButton('Cancel', callback_data=data.new(
            action='back_to_main',
            button_name='-'))
        all_buttons.add(cancel)
    return all_buttons


def drop_buttons():
    drop_categories = InlineKeyboardButton('Drop categories',
                                           callback_data=data.new(action=
                                                                  'drop_category',
                                                                  button_name='-'))
    drop_expense = InlineKeyboardButton('Drop expenses',
                                        callback_data=data.new(action=
                                                               'drop_expenses',
                                                               button_name='-'))
    """
    delete_single_expense = InlineKeyboardButton('Delete expense',
                                                 callback_data=data.new(
                                                     action =
                                                     'delete_expense',
                                                 button_name = '-'))
                                                 """
    back_button = InlineKeyboardButton('Back',
                                       callback_data=data.new(action=
                                                              'back_to_main',
                                                              button_name='-'))
    dropers = InlineKeyboardMarkup(row_width=2).add(drop_categories,
                                                    drop_expense)
    dropers.add(back_button)
    return dropers


def delete_category(categories_list=None):
    categories = InlineKeyboardMarkup(row_width=2)
    for category in categories_list:
        buton1 = InlineKeyboardButton(str(category),
                                      callback_data=data.new(action='delete',
                                                             button_name=str(
                                                                 category)))
        categories.add(buton1)
    back_button = InlineKeyboardButton('Back', callback_data=data.new(action=
                                                                      'back_to_main',
                                                                      button_name=
                                                                      'back'))
    categories.add(back_button)
    return categories


def choose_category_expense(categories_list=None):
    categories = InlineKeyboardMarkup(row_width=2)
    for category in categories_list:
        buton1 = InlineKeyboardButton(str(category),
                                      callback_data=data.new(action='choose',
                                                             button_name=str(
                                                                 category)))
        categories.add(buton1)
    back_button = InlineKeyboardButton('Back', callback_data=data.new(action
                                                                      ='back_to_main'
                                                                       '',
                                                                      button_name=
                                                                      'back'))
    categories.add(back_button)
    return categories


def last_five(last_expenses=None):
    expenses = InlineKeyboardMarkup(row_width=2)
    for expense in last_expenses:
        last_expense=last_expenses[expense]
        button_title = last_expense['category']+' '+\
                       last_expense['merchandise']+' '+\
                       str(last_expense['price'])
        button = InlineKeyboardButton(button_title,
                                      callback_data=data.new(
            action='choose_and_delete', button_name=str(last_expense['expense_id'])))
        expenses.add(button)
    back_button = InlineKeyboardButton('Back', callback_data=data.new(action
                                                                      ='back_to_main',
                                                                      button_name=
                                                                      'back'))
    expenses.add(back_button)
    return expenses

# res = ReplyKeyboardRemove()

# при нажатии кнопки поменять состояние
