from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

"""

button_hi = KeyboardButton('Hello')
greet_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_button.add(button_hi)
"""

categories_button = InlineKeyboardButton('Show my categories',
                                         callback_data='categories')
add_category_button = InlineKeyboardButton('Add category',
                                           callback_data='add category')
add_expence_button = InlineKeyboardButton('Add expence', callback_data='add '
                                                                       'expence')
all_buttons = InlineKeyboardMarkup(row_width=2).add(categories_button)

help_button = InlineKeyboardButton('Help',
                                   callback_data='help')
info = InlineKeyboardButton('Information', callback_data='info')

all_buttons.row(info, help_button)
all_buttons.add(add_category_button)

# при нажатии кнопки поменять состояние
