import asyncio
import aiomysql
from database.config import DatabaseConfig
from database.sql_queries import SqlQueries
"""
вынести настройки в датабейс конфиг, тогда к ним можно будет обращаться из обоих файлов без конфликтов
создание БД необходимо вынести в докер, туда скопировать скрипт создающий ба и таблицы
"""

class DataBase(DatabaseConfig):
    def __init__(self):
        super().__init__()
        self.sql = SqlQueries

    async def up_service(self):
        # todo автоматическое поднятие баз при запуске, использовать в другом скрипте юзающемсяв баш-скрипте
        pass

    async def run_sql(self, query: str):
        connection = await aiomysql.connect(host=self.host, user=self.bot_user,
                                            password='Khamul_password', port=self.port)
        cur = await connection.cursor()
        await cur.execute(query)
        connection.close()
        print('Connection closed')

    async def create_backend_database(self):
        await self.run_sql(self.sql.create_database(db_name=self.backend_db_name))

    async def create_finance_database(self):
        await self.run_sql(self.sql.create_database(db_name=self.finance_db_name))

    async def create_table(self, query: str):
        await self.run_sql(query)

    async def create_user_category(self, user_id, category: str):
        user_categories = await self.select_user_categories(user_id)
        if not user_categories:
            await self.run_sql(self.sql.create_category(category, user_id))
            return True
        else:
            if category not in user_categories:
                await self.run_sql(self.sql.create_category(category, user_id))
                return True
            else:
                return False

    async def select_user_categories(self, user_id: int):
        a = await self.run_sql(self.sql.select_categories(self, user_id))
        print(a)

    async def drop_databases(self):

        await self.run_sql("USE bot_backend; DROP TABLE categories;")
        await self.run_sql("USE bot_finance; DROP TABLE expenses;")
        await self.run_sql("USE bot_backend; DROP TABLE users;")
        await self.run_sql(self.sql.drop_database(self.backend_db_name))
        await self.run_sql(self.sql.drop_database(self.finance_db_name))


if __name__ == '__main__':
    ad = DataBase()
    #asyncio.get_event_loop().run_until_complete(ad.create_backend_database())
    #asyncio.get_event_loop().run_until_complete(ad.create_finance_database())
    #asyncio.get_event_loop().run_until_complete(ad.create_table(query=ad.sql.ct_users(ad.backend_db_name)))
    #asyncio.get_event_loop().run_until_complete(ad.create_table(query=ad.sql.ct_categories(ad.backend_db_name)))
    #asyncio.get_event_loop().run_until_complete(ad.create_table(query=ad.sql.ct_expenses(ad.finance_db_name)))
    asyncio.get_event_loop().run_until_complete(ad.run_sql("USE bot_backend; INSERT INTO users VALUES (123, 1.2)"))
    #asyncio.get_event_loop().run_until_complete(ad.connect())
    #asyncio.get_event_loop().run_until_complete(ad.drop_databases())
