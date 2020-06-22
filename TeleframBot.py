import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import utils
import operationsMongo
import message_parser
import createMongo
import msganswers
from config import TOKEN
import buttons
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
#storage = Mongo
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
#сохранять состояния в монго



@dp.callback_query_handler(lambda callback: callback.data, state="*")
async def process_callback_button(callback_query: types.CallbackQuery):
    #Перейти на кнопки везде где это возможно
    state = dp.current_state(user=callback_query.from_user.id)
    user_id = callback_query.from_user.id
    code = callback_query.data
    print(code)
    if code == 'categories':
        #categ = operationsMongo.show_user_categories(user_id)
        if await createMongo.check_collection_exists(user_id):

            await bot.send_message(callback_query.from_user.id,await
                                   operationsMongo.show_user_categories(user_id))
        else:
            bot.send_message(callback_query.from_user.id, msganswers.user_hasnt_categoty)
    elif code == 'help':
        await bot.send_message(callback_query.from_user.id, callback_query.from_user.first_name)
    elif code == 'info':
        await bot.send_message(callback_query.from_user.id, await
        msganswers.manual_text(callback_query.from_user.first_name))
    elif code == 'add category':
        #pass
        await utils.ToAdd.add_category.set()
        #await state.finish()

#отрисовываем кнопки из buttons.py
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(msganswers.start, reply_markup=buttons.all_buttons)

#обработка трат должна производится без
@dp.message_handler(state=utils.ToAdd.add_category,
                    content_types=types.ContentType.TEXT)
async def process_add_category(message : types.Message, state: FSMContext):

    user_id = message.from_user.id
    text = message.text
    #print(text)
    answer = await createMongo.check_before_addition(user_id, text=text)
    text = await message_parser.parse_user_input(text, flag=True)
    ans = await msganswers.add_category_answers(*answer)
    if ans == 'category already exists':
        await message.reply(ans)
        await state.finish()
    else:
        await operationsMongo.add_user_category(user_id, text.capitalize())
        await message.reply('Категория создана')
        await state.finish()
##########################################
@dp.message_handler(commands=['drop'])
async def process_drop_user_collection(message: types.Message):
    user_id = message.from_user.id
    await createMongo.drop_user_expenses(user_id)
    await message.reply('Ваши грехи позабыты')


@dp.message_handler(commands=['dropcat'])
async def process_drop_user_categories(message: types.Message):
    user_id = message.from_user.id
    await createMongo.drop_user_categories(user_id)
    await message.reply('Ваши категории позабыты')


@dp.message_handler(commands=['help'])##################
async def process_help_command(message: types.Message):
    await message.answer(msganswers.manual_text(message.from_user.first_name))
########################################

@dp.message_handler(commands=['categories'])##############
async def categories_command(message: types.Message):
    user_id = message.from_user.id
    if await createMongo.check_collection_exists(user_id):
        await message.answer(await operationsMongo.show_user_categories(
            user_id))
    else:
        await message.answer(msganswers.user_hasnt_categoty)


@dp.message_handler(commands=['commandslist'])
async def commands_list(message: types.Message):
    await message.answer(msganswers.bot_commandslist)


@dp.message_handler(commands=['dellast'])
async def delete_last_expence(message: types.Message):
    user_id = message.from_user.id
    delete_expenxe = await operationsMongo.delete_last_expence(user_id)
    await message.answer(delete_expenxe)


@dp.message_handler(commands=['info'])#################
async def process_info_command(message: types.Message):
    await message.reply('INFO')


@dp.message_handler(commands=['dreport'])
async def create_daily_report(msg: types.Message):
    # date = str(msg.date)[:10]
    user_id = msg.from_user.id
    report = await operationsMongo.create_daily_report(user_id)
    await msg.answer(report)


@dp.message_handler()
async def echo_message(msg: types.Message):
    text = msg.text
    parse_input_elements = await message_parser.parse_user_input(text)
    category, goods, money = parse_input_elements
    user_id = msg.from_user.id
    date = str(msg.date)
    check_user_input = await operationsMongo.check_user_input(category, money,
                                                              user_id)
    category = category.capitalize()
    ans = await msganswers.add_expence_answers(*check_user_input,
                                               category=category, text=text)
    if ans == msganswers.expense_added:
        await operationsMongo.add_expense(user_id, date, category, goods,
                                          money)
    await msg.answer(ans)


if __name__ == '__main__':
    executor.start_polling(dp)