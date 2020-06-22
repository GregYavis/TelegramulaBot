import datetime

import createMongo
from createMongo import client
from createMongo import client_constants #connect to db using .db_client

REPORT_FORMAT = "{category}, {goods}, {price}"
REPORT_FORMAT2 = "{id}, {price}, {date}, {category}, {goods}"


async def add_expense(user_id: int, date: str, category: str, goods: str,
                      money: str):
    collection = client_constants.db_client['expense' + str(user_id)]
    insert = {'expense': money, 'date': date, 'category': category, 'goods':
        goods}
    await collection.insert_one(insert)
    client.close()


async def add_user_category(user_id: int, text):
    collection = client_constants.db_client[str('category') + str(user_id)]
    category = {'category': text}
    await collection.insert_one(category)
    client.close()


async def check_user_input(category, price, user_id: int, add_flag=False,
                           price_flag=False):
    category = category.capitalize()
    collection = client_constants.db_client['category' + str(user_id)]
    document = {'category': category}
    count = await createMongo.document_exists(collection, document)
    if count:
        add_flag = True
    if price.isdigit():
        price_flag = True
    return add_flag, price_flag


async def show_user_categories(user_id: int):
    user_categories = ''
    collection = client_constants.db_client['category' + str(user_id)]
    cursor = collection.find()
    for document in await cursor.to_list(None):
        user_category = document['category'].capitalize()
        user_categories += user_category + '\n'
    return user_categories


async def delete_last_expence(user_id: int):
    collection = client_constants.db_client['expense' + str(user_id)]
    list_is = await create_daily_report(user_id, delete_flag=True)
    if list_is == []:
        return "Отчет пуст"
    else:
        last = list_is[-1].split(',')
        await collection.delete_one({'date': last[2].lstrip()})
        return "Удалено {0}".format(last)


async def create_daily_report(user_id: int, delete_flag=False):
    report_template = REPORT_FORMAT
    report_template2 = REPORT_FORMAT2
    day_reprt = []
    today = str(datetime.date.today())[:10]  # magic number
    collection = client_constants.db_client['expense' + str(user_id)]
    print(collection)
    for document in await collection.find().to_list(None):
        values = document.values()
        _, price, date, category, goods = values
        if delete_flag:
            if date[:10] == today:
                report = report_template2.format(id=_, price=price,
                                                 date=date, category=category,
                                                 goods=goods)
                day_reprt.append(report.capitalize())
        else:
            if date[:10] == today:
                report = report_template.format(category=category, goods=goods,
                                                price=price)
                day_reprt.append(report.capitalize())
    if day_reprt == []:
        return "Отчёт за сегодняшний день пуст"
    else:
        return day_reprt
