from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

items_for_add = ['Category', 'Expence']
from aiogram.utils.helper import Helper, HelperMode, ListItem


class User_states(StatesGroup):
    #mode = HelperMode.snake_case
    add_category = State()
    choose_category = State()
    add_expense = State()
    #drop_category = State()


