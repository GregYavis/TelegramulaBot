import logging
from db_config import DataBaseConfig
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

client_constants = DataBaseConfig('DataBase')
print(client_constants)
client = DataBaseConfig().client
print(client)
db = client_constants.db_client
print(db)

"""
client = db_config.ConnectToBase()
client.db_client()
client = client.cli
DB_names = db_config.ConnectToBase()
DB_names.db_setname('DataBase')
db = client[DB_names.name]  # Name of dataBase
"""

# collection = db['category']

async def document_exists(collection, document={}):
    count = await collection.count_documents(document)
    if count > 0:
        return True
    else:
        return False


async def check_collection_exists(user_id: int):
    collection_name = 'category' + str(user_id)

    print(collection_name)
    exsts = collection_name in await db.list_collection_names()
    return exsts


async def check_before_addition(user_id: int, text=None):
    collection_name = 'category' + str(user_id)

    exsts = collection_name in await db.list_collection_names()
    if exsts:
        collection_exists_flag = True
    else:
        collection_exists_flag = False
        category_exists_flag = False
        return collection_exists_flag, category_exists_flag
    import message_parser
    text = await message_parser.parse_user_input(text, flag=True)
    collection = db[str('category') + str(user_id)]
    document = {'category': text}
    count = await document_exists(collection, document)
    if count:
        category_exists_flag = True
    else:
        collection_exists_flag = True
        category_exists_flag = False
        return collection_exists_flag, category_exists_flag

    return collection_exists_flag, category_exists_flag


async def drop_user_expenses(user_id: int):
    collection = client_constants.db_client['expense' + str(user_id)]
    if await document_exists(collection):
        await collection.drop()
        client.close()


async def drop_user_categories(user_id: int):
    collection = client_constants.db_client['category'+str(
        user_id)]
    if await document_exists(collection):
        await collection.drop()
        client.close()
