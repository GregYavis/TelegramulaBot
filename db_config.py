import motor.motor_asyncio


class DataBaseConfig:

    def collection_name(self, name=None, user_id=None):
        if user_id == None:
            self.user_collection_name = name
        else:
            self.user_collection_name = name + user_id
        #self.connect_to_collection = self.db_client[str(name)]
    def __init__(self, db_name=None):
        self.client = motor.motor_asyncio.AsyncIOMotorClient()
        self.name = db_name
        self.db_client = self.client[str(db_name)]


"""
db_name = 'DataBase'


client_constants = DataBaseConfig()
client_constants.db_client_constants(db_name=db_name)
client = client_constants.client
db = client_constants.db_client

client_constants.collection_name('category')
category = client_constants.user_collection_name


client_constants.collection_name('expense')
expense = client_constants.user_collection_name

<db_config.DataBaseConfig object at 0x7f1f9ec02e10>
AsyncIOMotorClient(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=False, driver=DriverInfo(name='Motor', version='2.1.0', platform=None)))
AsyncIOMotorDatabase(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=False, driver=DriverInfo(name='Motor', version='2.1.0', platform=None)), 'DataBase'))
"""