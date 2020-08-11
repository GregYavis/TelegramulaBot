import asyncio
import datetime
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from utils import User_states
from postgres import PostgresQuery
from parsers import function_to_lamda_handler, parse_user_expence, \
    digits_parser
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

postgres = PostgresQuery()
button_action = CallbackData('content', 'action', 'button_name')


@dp.callback_query_handler(button_action.filter(action='show_categories'))
async def process_show_categories(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    answer = ''
    if not await postgres.select_user_categories(user_id=user_id):
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text="У вас ещё нет ни одной категории")
    else:
        for category in await postgres.select_user_categories(user_id=user_id):
            answer += category + '\n'
        # тут можно протестировать отрисовку большого количества кнопок
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=answer)


@dp.callback_query_handler(button_action.filter(action='Utility'))
async def process_show_utility(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.utility_buttons(),
                                text='Другие функции')


@dp.callback_query_handler(button_action.filter(action='get_report'))
async def process_get_report(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    report = await postgres.get_report(user_id=user_id)
    if not report:
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text='Вы ещё ни на что не тратились')
    else:
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=report)


@dp.callback_query_handler((button_action.filter(action='get_day_expenses')))
async def process_get_day(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    date = datetime.datetime.now().date()
    message = await postgres.get_day(user_id=user_id, date=date)
    if not message:
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text='Сегодня вы ни на что не тратились')
    else:
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=message)


@dp.callback_query_handler(button_action.filter(action='back_to_main'),
                           state='*')
async def process_show_drops(callback_query: types.CallbackQuery,
                             state: FSMContext):
    user_id = callback_query.from_user.id
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.all_buttons(),
                                text='Действие отменено')
    await state.finish()


@dp.callback_query_handler(button_action.filter(action='get_balance'))
async def process_get_balance(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    balance = await postgres.get_balance(user_id=user_id)
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.utility_buttons(),
                                text=balance)


# User_states.deleting

@dp.callback_query_handler(button_action.filter(action='add_category'),
                           state='*')
async def process_add_category(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    global msg_id
    msg_id = callback_query.message.message_id
    await User_states.add_category.set()
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.only_back_button(),
                                text=answers.add_category)


@dp.callback_query_handler(button_action.filter(action='add_expense'))
async def process_add_expense(callback_query: types.CallbackQuery):
    # print(callback_query.data.split(':'))
    user_id = callback_query.from_user.id
    postgres = PostgresQuery()
    if not await postgres.select_user_categories(user_id):
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text='Вы ещё не создали ни одной категории')
    else:
        user_categories = await postgres.select_user_categories(user_id)
        keyboard = buttons.choose_category_expense(
            categories_list=user_categories)
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
    if not await postgres.get_balance(user_id=user_id):
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text='Вы не задали начальный баланс')
    else:
        await User_states.choose_category.set()
        async with state.proxy() as data:
            data['category'] = callback_query.data.split(':')[2]
        await User_states.next()
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons.all_buttons(),
                                    text='Введите цифру')


@dp.callback_query_handler(button_action.filter(action='drop'), state='*')
async def process_show_drops(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await User_states.deleting.set()

    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.drop_buttons(),
                                text='Выбор')


@dp.callback_query_handler(button_action.filter(action='drop_expenses'),
                           state='*')
async def process_show_last_five(callback_query: types.CallbackQuery,
                                 state: FSMContext):
    user_id = callback_query.from_user.id
    msg_id = callback_query.message.message_id
    if not await postgres.get_last_five(user_id):
        await state.finish()
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=msg_id,
            reply_markup=buttons.all_buttons(),
            text='Ваши траты уже удалены либо ещё отсутствуют')
    else:
        last_five_expenses = await postgres.get_last_five(user_id)
        keyboard = buttons.last_five(last_five_expenses)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=msg_id,
                                    reply_markup=keyboard,
                                    text='Выбор траты для удаления')


@dp.callback_query_handler(button_action.filter(action='choose_and_delete'),
                           state='*')
async def process_delete_expense_from_last_five(
        callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    expense_id = callback_query.data.split(':')[2]
    await postgres.delete_expense(expense_id=expense_id, user_id=user_id)
    await state.finish()
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.all_buttons(),
                                text='Запись удалена')


@dp.callback_query_handler(button_action.filter(action='drop_category'),
                           state='*')
async def process_choose_category_delete(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_categories = await postgres.select_user_categories(user_id)
    keyboard = buttons.delete_category(categories_list=user_categories)
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboard,
                                text='Выберите категорию для удаления')


@dp.callback_query_handler(button_action.filter(action='delete'), state='*')
async def process_delete_category(callback_query: types.CallbackQuery,
                                  state: FSMContext):
    user_id = callback_query.from_user.id
    category = callback_query.data.split(':')[2]
    await postgres.delete_user_category(user_id=user_id, category=category)
    await state.finish()
    await bot.edit_message_text(chat_id=user_id,
                                message_id=callback_query.message.message_id,
                                reply_markup=buttons.all_buttons(),
                                text='Категория {0} удалена'.format(category))


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message):
    await message.answer(answers.start, reply_markup=buttons.all_buttons())


@dp.message_handler(state=User_states.add_category)
async def process_add_category(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    category = message.text
    if await postgres.select_user_categories(user_id) is False:
        await postgres.create_user_category(user_id=user_id, category=category)
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

    else:
        await postgres.create_user_category(user_id=user_id, category=category)
        await state.finish()
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=msg_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=answers.category_added)


@dp.callback_query_handler(button_action.filter(action='balance'), state='*')
async def process_balance(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    global msg_id
    msg_id = callback_query.message.message_id
    if not await postgres.get_balance(user_id=user_id):
        await User_states.set_balance.set()
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=msg_id,
                                    reply_markup=buttons.only_back_button(),
                                    text='Введите значение баланса')
    else:
        # current_balance = await postgres.get_balance(user_id=user_id)
        await User_states.update_balance.set()
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=msg_id,
                                    reply_markup=buttons.only_back_button(),
                                    text='Введите значение которое добавится к текущему балансу')


@dp.message_handler(lambda message: not bool(digits_parser(message.text)),
                    state=User_states.set_balance)
async def process_input_invalid(message: types.Message):
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=msg_id,
                                reply_markup=buttons.only_back_button(),
                                text='Неверный формат баланса')


@dp.message_handler(state=User_states.set_balance)
async def process_write_balance(message: types.Message, state: FSMContext):
    balance_input = message.text
    user_id = message.from_user.id
    await postgres.init_balance(user_id=user_id, balance=balance_input)
    await state.finish()
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=msg_id,
                                reply_markup=buttons.only_back_button(),
                                text='Записано' + ' ' + message.text)


@dp.message_handler(lambda message: not bool(digits_parser(message.text)),
                    state=User_states.update_balance)
async def process_input_invalid(message: types.Message):
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=msg_id,
                                reply_markup=buttons.only_back_button(),
                                text='Неверный формат обновления')


@dp.message_handler(state=User_states.update_balance)
async def process_write_balance(message: types.Message, state: FSMContext):
    update = message.text
    user_id = message.from_user.id
    await postgres.update_balance(user_id=user_id, update=update)
    await state.finish()
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=msg_id,
                                reply_markup=buttons.only_back_button(),
                                text='Записано' + ' ' + message.text)


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
async def process_record_user_expense(message: types.Message,
                                      state: FSMContext):
    await state.update_data(expence=message.text)
    # добавляем трату к категории к которой она относится
    user_id = message.from_user.id
    date = datetime.datetime.now().date()
    async with state.proxy() as data:
        bot_message = data['category'] + ' ' + data['expence']
        user_input = await parse_user_expence(data['expence'])
        expense_data = {'user_id': user_id,
                        'category': data['category'],
                        'merchandise': user_input['merchandise'],
                        'price': user_input['price'],
                        'date': date
                        }
        await postgres.add_user_expense(expense_data)
        # передать 'expence' в парсер, выделить в нём цену, большая цифра -
        # это цена, остальное - товар/услуга
        await bot.edit_message_text(chat_id=message.from_user.id,
                                    message_id=msg_id,
                                    reply_markup=buttons.all_buttons(),
                                    text=bot_message)
    await state.finish()


@dp.message_handler(commands=['help'])  ##################
async def process_help_command(message: types.Message):
    await message.answer(answers.manual_text(message.from_user.first_name))


@dp.message_handler(commands=['commandslist'])
async def commands_list(message: types.Message):
    await message.answer(answers.bot_commandslist)


if __name__ == '__main__':
    executor.start_polling(dp)
