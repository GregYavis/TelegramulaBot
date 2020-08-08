import asyncio
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from utils import User_states
from postgres import Postgres_Query
from parsers import function_to_lamda_handler, parse_user_expence
import answers
from config import TOKEN
import buttons
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

codes = ['categories', 'add category', 'add expense', 'cancel', 'drop',
         'back_to_main', 'drop_categories', 'drop_expenses']

postgres = Postgres_Query()
button_action = CallbackData('content', 'action', 'button_name')


@dp.callback_query_handler(button_action.filter(button_name='show_categories'))
async def process_show_categories(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    postgres = Postgres_Query()
    answer = ''
    for category in await postgres.select_user_categories(
            user_id=user_id):
        answer += category + '\n'
    # тут можно протестировать отрисовку большого количества кнопок
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.all_buttons(),
                                text=answer)


@dp.callback_query_handler(button_action.filter(button_name='add_category'))
async def process_add_category(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    global msg_id
    msg_id = callback_query.message.message_id
    await User_states.add_category.set()
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.all_buttons(
                                    cancel_button=True),
                                text=answers.add_category)


@dp.callback_query_handler(button_action.filter(button_name='add_expense'))
async def process_add_expense(callback_query: types.CallbackQuery):
    # print(callback_query.data.split(':'))
    user_id = callback_query.from_user.id

    postgres = Postgres_Query()
    user_categories = await postgres.select_user_categories(user_id)

    keyboard = buttons.choose_category_expense(categories_list=user_categories)

    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboard,
                                text='Выберите категорию')


@dp.callback_query_handler(button_action.filter(action='choose'))
async def process_choose_category_expense(callback_query: types.CallbackQuery,
                                          state: FSMContext):
    # await state.update_data(category=callback_query.data.split(':')[2])
    user_id = callback_query.from_user.id
    global msg_id
    msg_id = callback_query.message.message_id
    await User_states.choose_category.set()
    async with state.proxy() as data:
        data['category'] = callback_query.data.split(':')[2]
    await User_states.next()
    await bot.edit_message_text(chat_id=user_id,
                                message_id=msg_id,
                                reply_markup=buttons.all_buttons(),
                                text='Введите цифру')


@dp.callback_query_handler(button_action.filter(button_name='drop'))
async def process_show_drops(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    msg_id = callback_query.message.message_id
    await bot.edit_message_text(chat_id=user_id,
                                message_id=msg_id,
                                reply_markup=buttons.drop_buttons(),
                                text='Выбор')


@dp.callback_query_handler(button_action.filter(button_name='drop_categories'))
async def process_choose_category_delete(callback_query: types.CallbackQuery):
    postgres = Postgres_Query()
    user_id = callback_query.from_user.id
    user_categories = await postgres.select_user_categories(user_id)
    keyboard = buttons.delete_category(categories_list=user_categories)
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboard,
                                text='Выберите категорию для удаления')


@dp.callback_query_handler(button_action.filter(action='delete'))
async def process_delete_category(callback_query: types.CallbackQuery):
    postgres = Postgres_Query()
    user_id = callback_query.from_user.id
    category = callback_query.data.split(':')[2]
    await postgres.delete_user_category(user_id=user_id, category=category)
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.all_buttons(),
                                text='Категория {} удалена'.format(category))


@dp.callback_query_handler(button_action.filter(action='back_to_main'))
async def process_show_drops(callback_query: types.CallbackQuery,
                             state: FSMContext):
    user_id = callback_query.from_user.id
    await state.finish()
    # user_categories = await postgres.select_user_categories(user_id)
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.all_buttons(),
                                text='Действие отменено')

    """
    user_id = callback_query.from_user.id
    await User_states.choose_category.set()
    postgres = Postgres_Query()
    user_categories = await postgres.select_user_categories(user_id)
    keyboard = buttons.choose_category_to_expense(
        categories_list=user_categories)

    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboard,
                                text='Выберите категорию')"""


"""
"""
"""
@dp.callback_query_handler(button_action.filter(action='choose_category'),state=User_states.choose_category)
async def process_add_category(callback_query: types.CallbackQuery, state: FSMContext):
    print('choose')
    await state.update_data(category=callback_query.data)
    print(callback_query)
    #await User_states.next()
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.all_buttons(),
                                text='Введите цифру')
"""
"""
    elif code == 'add expense':
        postgres = Postgres_Query()
        user_categories = await postgres.select_user_categories(user_id)
        keyboard = buttons.delete_categories(categories_list=user_categories)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=keyboard,
                                    text='Выберите категорию')

        await User_states.choose_category.set()

    elif code == 'cancel':
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=answers.start)

    elif code == 'drop':
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.drop_buttons(),
                                    text=answers.drop)
    elif code == 'back_to_main':
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=answers.start)
        await state.finish()

    elif code == 'drop_categories':
        # передать как аргумент от
        postgres = Postgres_Query()
        user_categories = await postgres.select_user_categories(user_id)
        keyboard = buttons.delete_categories(categories_list=user_categories)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=keyboard,
                                    text='Выберите категорию для удаления')
        await User_states.drop_category.set()
        # await process_drop_user_categories(user_id, msg_id)

    elif code not in codes:

        # await User_states.choose_category.set()
        await User_states.next()
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text='Введите цифру')"""
"""
        elif code == 'drop_expenses':
        await process_drop_user_expenses(user_id, msg_id)
"""


# отрисовываем кнопки из buttons.py


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(answers.start, reply_markup=buttons.all_buttons())


@dp.message_handler(state=User_states.add_category)
async def process_add_category(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    category = message.text
    postgres = Postgres_Query()

    if await postgres.select_user_categories(user_id) is False:
        await postgres.create_user_category(user_id=user_id,
                                            category=category)
        await state.finish()
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=msg_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=answers.category_added)


    elif category in await postgres.select_user_categories(user_id):
        await state.finish()
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=msg_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=answers.category_exists)
        return

    else:
        await postgres.create_user_category(user_id=user_id,
                                            category=category)
        await state.finish()
        # await bot.edit_message_text(chat_id=user_id,
        # message_id=message.forward_from_chat)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=msg_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=answers.category_added)


# реализована проверка на наличие цифры в строке
# Подумать над проверкой на содержание более чем одной цифры
# Можно так же проверить наличие пробелов, если они есть - значит можно
# предположить что в строке отделены товар/услуга и цена

@dp.message_handler(lambda message: function_to_lamda_handler(message.text),
                    state=User_states.add_expense)
async def process_input_invalid(message: types.Message):
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=msg_id,
                                reply_markup=buttons.all_buttons(),
                                text='неверный формат')


# and
# если подразумевается что-то с объёмом, то должно быть как минимум две цифры

@dp.message_handler(state=User_states.add_expense)
async def process_test(message: types.Message, state: FSMContext):
    await state.update_data(expence=message.text)  # добавляем трату к
    # категории к которой она относится
    async with state.proxy() as data:
        bot_message = data['category'] + ' ' + data['expence']
        print(bot_message)
        await parse_user_expence(data['expence'])
        # передать 'expence' в парсер, выделить в нём цену, большая цифра -
        # это цена, остальное - товар/услуга
        await bot.edit_message_text(chat_id=message.from_user.id,
                                    message_id=msg_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=bot_message)
    await state.finish()


"""

async def process_drop_user_expenses(user_id, msg_id):

    await bot.edit_message_text(chat_id=user_id, message_id=msg_id,
                                reply_markup=buttons.drop_buttons(),
                                text=answers.drop_expenses)
"""

"""
@dp.message_handler(state=User_states.add_expense)
async def process_drop_user_categories(user_id, msg_id, state: FSMContext):
    pass
    await postgres.drop_user_categories(user_id=user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=msg_id,
                                reply_markup=buttons.all_buttons(),
                                text=answers.drop_categories)"""
"""

@dp.message_handler(commands=['help'])  ##################
async def process_help_command(message: types.Message):
    await message.answer(answers.manual_text(message.from_user.first_name))


@dp.message_handler(commands=['commandslist'])
async def commands_list(message: types.Message):
    await message.answer(answers.bot_commandslist)


"""
"""
# переделать так как он удаляет последнюю только за текущий день
@dp.message_handler(commands=['dellast'])
async def delete_last_expence(message: types.Message):
    user_id = message.from_user.id
    delete_expense = await operationsMongo.delete_last_expence(user_id)
    await message.answer(delete_expense)


@dp.message_handler(commands=['dreport'])
async def create_daily_report(msg: types.Message):
    # date = str(msg.date)[:10]
    user_id = msg.from_user.id
    report = await operationsMongo.create_daily_report(user_id)
    await msg.answer(report)
"""

# Ранее обрабатывал сообщения, вскоре можно убрать

if __name__ == '__main__':
    executor.start_polling(dp)
