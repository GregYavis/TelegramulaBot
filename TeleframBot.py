import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import utils
from utils import User_states
import operationsMongo
import message_parser
import createMongo
import answers
from config import TOKEN
import buttons
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
# storage = Mongo
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


# сохранять состояния в монго

@dp.callback_query_handler(lambda callback: callback.data, state="*")
async def process_callback_button(callback_query: types.CallbackQuery):
    # Перейти на кнопки везде где это возможно
    global msg_id
    state = dp.current_state(user=callback_query.from_user.id)
    user_id = callback_query.from_user.id
    code = callback_query.data
    msg_id = callback_query.message.message_id

    print(code)
    if code == 'categories':
        # categ = operationsMongo.show_user_categories(user_id)
        if await createMongo.check_collection_exists(user_id):

            await bot.send_message(callback_query.from_user.id, await
            operationsMongo.show_user_categories(user_id))
        else:
            await bot.send_message(user_id, answers.user_hasnt_categoty)
    elif code == 'add category':
        # pass

        await User_states.add_category.set()
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id,
                                    reply_markup=buttons.all_buttons(
                                        cancel_button=True),
                                    text=answers.add_category)

        # await state.finish()
    elif code == 'add expense':
        await User_states.add_expense.set()
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id,
                                    reply_markup=buttons.all_buttons(
                                        cancel_button=True), text=answers.start)

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
    elif code == 'drop_categories':
        await process_drop_user_categories(user_id, msg_id)
    elif code == 'drop_expenses':
        await process_drop_user_expenses(user_id, msg_id)
    # отрисовываем кнопки из buttons.py


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(answers.start, reply_markup=buttons.all_buttons())


@dp.message_handler(state=User_states.add_category)
async def process_add_category(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    text = message.text
    # print(text)

    answer = await createMongo.check_before_addition(user_id, text=text)
    text = await message_parser.parse_user_input(text, flag=True)
    ans = await answers.add_category_answers(*answer)
    if ans == 'category already exists':
        await message.reply(ans)
        await state.finish()
    else:
        await operationsMongo.add_user_category(user_id, text.capitalize())
        await message.answer('Категория создана')
        await state.finish()


@dp.message_handler(state=User_states.add_expense)
async def process_add_expense(message: types.Message, state: FSMContext):
    text = message.text
    parse_input_elements = await  message_parser.parse_user_input(text)
    category, goods, money = parse_input_elements
    user_id = message.from_user.id
    date = str(message.date)
    check_user_input = await operationsMongo.check_user_input(category,
                                                              money, user_id)
    category = category.capitalize()
    ans = await answers.add_expence_answers(*check_user_input,
                                            category=category, text=text)
    if ans == answers.expense_added:
        await operationsMongo.add_expense(user_id, date, category, goods,
                                          money)
        await state.finish()
    await message.answer(ans)
    await state.finish()


##########################################

async def process_drop_user_expenses(user_id, msg_id):
    await createMongo.drop_user_expenses(user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=msg_id,
                                reply_markup=buttons.drop_buttons(),
                                text=answers.drop_expenses)


async def process_drop_user_categories(user_id, msg_id):
    await createMongo.drop_user_categories(user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=msg_id,
                                    reply_markup=buttons.drop_buttons(),
                                    text=answers.drop_categories)


@dp.message_handler(commands=['help'])  ##################
async def process_help_command(message: types.Message):
    await message.answer(answers.manual_text(message.from_user.first_name))


@dp.message_handler(commands=['commandslist'])
async def commands_list(message: types.Message):
    await message.answer(answers.bot_commandslist)

#переделать так как он удаляет последнюю только за текущий день
@dp.message_handler(commands=['dellast'])
async def delete_last_expence(message: types.Message):
    user_id = message.from_user.id
    delete_expenxe = await operationsMongo.delete_last_expence(user_id)
    await message.answer(delete_expenxe)


@dp.message_handler(commands=['dreport'])
async def create_daily_report(msg: types.Message):
    # date = str(msg.date)[:10]
    user_id = msg.from_user.id
    report = await operationsMongo.create_daily_report(user_id)
    await msg.answer(report)


# Ранее обрабатывал сообщения, вскоре можно убрать

if __name__ == '__main__':
    executor.start_polling(dp)
