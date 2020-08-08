from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.callback_data import CallbackData

data = CallbackData('content','action','button_name')


def all_buttons(cancel_button=False):
    categories_button = InlineKeyboardButton('Show my categories',
                                             callback_data=data.new(action =
                                                                    'show',
                                                 button_name='show_categories'))
    add_category_button = InlineKeyboardButton('Add category',
                                               callback_data=data.new(action =
                                                                      'add_cat',
                                                   button_name='add_category'))
    add_expense_button = InlineKeyboardButton('Add expence',
                                              callback_data=data.new(action =
                                                                     'add',
                                                  button_name='add_expense'))

    all_buttons = InlineKeyboardMarkup(row_width=3)
    all_buttons.add(add_category_button, add_expense_button)
    drop = InlineKeyboardButton('Drop', callback_data=data.new(action = 'drop',
                                                               button_name='drop'))
    all_buttons.add(drop, categories_button)
    if cancel_button:
        cancel = InlineKeyboardButton('Cancel', callback_data=data.new(
            action='back_to_main',
            button_name='-'))
        all_buttons.add(cancel)
    return all_buttons


def drop_buttons():
    drop_categories = InlineKeyboardButton('Drop categories',
                                           callback_data=data.new(action =
                                                                  'drop_category',
                                               button_name='drop_categories'))
    drop_expense = InlineKeyboardButton('Drop expenses',
                                        callback_data=data.new(action =
                                                               'drop_expenses',
                                            button_name='drop_expenses'))
    back_button = InlineKeyboardButton('Back',
                                       callback_data=data.new(action =
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
                                      callback_data=data.new(action = 'delete',
                                          button_name=str(category)))
        categories.add(buton1)
    back_button = InlineKeyboardButton('Back', callback_data=data.new(action =
                                                                      'back_to_main',
                                                                      button_name=
                                                                      'back'))
    categories.add(back_button)
    return categories


def choose_category_expense(categories_list=None):
    categories = InlineKeyboardMarkup(row_width=2)
    for category in categories_list:
        buton1 = InlineKeyboardButton(str(category),
                                      callback_data=data.new(action = 'choose',
                                          button_name=str(category)))
        categories.add(buton1)
    back_button = InlineKeyboardButton('Back', callback_data=data.new(action
                                                                      ='back_to_main'
                                                                      '',
                                                                      button_name=
                                                                      'back'))
    categories.add(back_button)
    return categories
# res = ReplyKeyboardRemove()

# при нажатии кнопки поменять состояние
