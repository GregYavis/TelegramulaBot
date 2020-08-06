from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

"""

button_hi = KeyboardButton('Hello')
greet_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_button.add(button_hi)
"""


def all_buttons(cancel_button=False):
    categories_button = InlineKeyboardButton('Show my categories',
                                             callback_data='categories')
    add_category_button = InlineKeyboardButton('Add category',
                                               callback_data='add category')
    add_expense_button = InlineKeyboardButton('Add expence',
                                              callback_data='add '
                                                            'expense')

    all_buttons = InlineKeyboardMarkup(row_width=3)
    all_buttons.add(add_category_button, add_expense_button)
    drop = InlineKeyboardButton('Drop', callback_data='drop')
    all_buttons.add(drop, categories_button)
    if cancel_button:
        cancel = InlineKeyboardButton('Cancel', callback_data='cancel')
        all_buttons.add(cancel)
    return all_buttons


def drop_buttons():
    drop_categories = InlineKeyboardButton('Drop categories',
                                           callback_data='drop_categories')
    drop_expense = InlineKeyboardButton('Drop expenses',
                                        callback_data='drop_expenses')
    back_button = InlineKeyboardButton('Back', callback_data='back_to_main')
    dropers = InlineKeyboardMarkup(row_width=2).add(drop_categories,
                                                    drop_expense)
    dropers.add(back_button)
    return dropers


def categories_buttons(categories_list=None):
    """    if clean:
        categories = ReplyKeyboardRemove()
    else:
        categories = ReplyKeyboardMarkup()
    if categories_list:
        for category in categories_list:
            button = KeyboardButton(str(category))
            categories.add(button)
    return categories"""

    categories = InlineKeyboardMarkup(row_width=2)
    for category in categories_list:
        buton1 = InlineKeyboardButton(str(category), callback_data=str(category))
        categories.add(buton1)
    back_button = InlineKeyboardButton('Back', callback_data='back_to_main')
    categories.add(back_button)
    return categories

# res = ReplyKeyboardRemove()

# при нажатии кнопки поменять состояние
