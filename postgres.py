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
            await self.connection.close()
            return selection
        else:
            await self.connection.execute(query)
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
        print(self.select_user_categories(user_id))
        """
        query_string = 'DROP TABLE IF EXISTS {0}'.format(
            'categories' + str(user_id))
        await self.query_execute(query_string)
        """
    async def delete_user_category(self, user_id: int, category):
        query_string = 'DELETE FROM {0} WHERE category=(''\'{1}\')'.format(
            'categories' + str(user_id), category)
        await self.query_execute(query_string)

    async def add_user_expense(self):
        pass


"""    async def parse_user_expence(self, text: str):
        self.parse_digits = [
            float(digit) for digit in self.digits_parser(text)]
        price = max(self.parse_digits)  # передаётся в таблицу
        splitted_input = text.split(' ')
        for element in splitted_input:
            if self.digits_parser(element):
                digit = float(self.digits_parser(element)[0])
                if price == digit:
                    splitted_input.pop(splitted_input.index(element))
        return 

    def digits_parser(self, string_input):
        self.parsed =  re.findall(
            '[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?',
            string_input)
        return self.parsed
"""
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
