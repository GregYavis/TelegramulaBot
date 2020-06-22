from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
items_for_add = ['Category', 'Expence']
from aiogram.utils.helper import Helper, HelperMode, ListItem
class ToAdd(StatesGroup):
    mode = HelperMode.snake_case
    add_category = State()
    TEST_STATE_1 = State()
