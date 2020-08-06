import asyncio
import asyncpg
import re


class Postgres_Query:
    async def query_execute(self, query, select=False):
        self.connection = await asyncpg.connect(user='postgres',
                                                database='finance',
                                                password='khamul')
        if select:
            selection = await self.connection.fetch(query)
            print('close')
            await self.connection.close()
            return selection
        else:
            await self.connection.execute(query)
            print('close')
        await self.connection.close()

    async def create_user_category(self, user_id: int, category):
        query_string = 'CREATE TABLE IF NOT EXISTS "{0}" ' \
                       '(category VARCHAR (50));' \
                       'INSERT INTO "{0}" (category) VALUES (''\'{1}\')'.format(
            'categories' + str(user_id), category)
        await self.query_execute(query_string)

    async def select_user_categories(self, user_id: int):
        query_string = 'SELECT * FROM {0}'.format('categories' + str(user_id))
        try:
            result = await self.query_execute(query=query_string, select=True)
            user_categories = [category[0] for category in result]
            return user_categories
        except asyncpg.exceptions.UndefinedTableError:
            return False  # return to check that user's table doesn't exists

    async def drop_user_categories(self, user_id: int):
        query_string = 'DROP TABLE IF EXISTS {0}'.format(
            'categories' + str(user_id))
        await self.query_execute(query_string)

    async def add_user_expense(self):

        pass

    async def parse_user_input(self, text):
        self.parse_input = re.split('\n', text)  # class list
        print(type(self.parse_input))

        # except asyncpg.exceptions.UndefinedTableError:


if __name__ == '__main__':
    open = Postgres_Query()
    # asyncio.get_event_loop().run_until_complete(open.open_connect())
    # asyncio.get_event_loop().run_until_complete(open.create_user_category(
    #   user_id=12345, category='PENIS'))
    asyncio.get_event_loop().run_until_complete(open.select_user_categories(
        302626122))
    # asyncio.get_event_loop().run_until_complete(open.drop_user_categories(
    #    302626122))
    # asyncio.get_event_loop().run_until_complete(open.close_connection())
