import asyncio

import asyncpg


class Postgres_Query:
    async def query_execute(self, query_string, select=False):
        self.connection = await asyncpg.connect(user='postgres',
                                                database='finance',
                                                password='khamul')
        if select:
            selection = await self.connection.fetch(query_string)
            await self.connection.close()
            return selection
        else:
            await self.connection.execute(query_string)
        await self.connection.close()

    async def create_user_category(self, user_id: int, category):
        query_string = 'CREATE TABLE IF NOT EXISTS "{0}" ' \
                       '(category VARCHAR (50));' \
                       'INSERT INTO "{0}" (category) VALUES (''\'{1}\')'.format(
            'categories' + str(user_id), category)
        await self.query_execute(query_string)

    async def select_user_categories(self, user_id: int):
        query = 'SELECT * FROM {0}'.format('categories' + str(user_id))
        try:
            result = await self.query_execute(query_string=query, select=True)
            user_categories = [category[0] for category in result]
            return user_categories
        except asyncpg.exceptions.UndefinedTableError:
            return False  # return to check that user's table doesn't exists

    async def delete_user_category(self, user_id: int, category):
        query = 'DELETE FROM {0} WHERE category=(''\'{1}\')'.format(
            'categories' + str(user_id), category)
        await self.query_execute(query)

    async def add_user_expense(self, expense_data):
        # user_id, category, goods, price, date = expense_data
        query = 'CREATE TABLE IF NOT EXISTS "{0}" ' \
                '(Id SERIAL,' \
                'category VARCHAR (100),' \
                'merchandise VARCHAR (100),' \
                'price FLOAT NOT NULL,' \
                'date_create date);' \
                'INSERT INTO "{0}" ' \
                'VALUES (DEFAULT,''\'{1}\',''\'{2}\',''\'{3}\',''\'{4}\')'.format(
            'expenses' + str(expense_data['user_id']),
            expense_data['category'],
            expense_data['merchandise'],
            expense_data['price'],
            expense_data['date'])
        await self.query_execute(query)

    async def get_last_five(self, user_id):
        query = 'SELECT * FROM {0} ORDER BY Id DESC LIMIT 5'.format(
            'expenses' + str(user_id))
        last_five = await self.query_execute(query_string=query, select=True)
        output = {}
        for expense in range(len(last_five)):
            # print(expense)
            output[str(expense)] = {
                'expense_id': last_five[expense]['id'],
                'category': last_five[expense]['category'],
                'merchandise': last_five[expense]['merchandise'],
                'price': last_five[expense]['price'],
                'date': last_five[expense]['date_create']}
        # print(output)
        # print(expense['category'], expense['goods'], expense['price'])
        return output

    async def get_day(self, user_id, date):
        query = 'SELECT * FROM {0} WHERE date_create = (''\'{1}\')'.format(
            'expenses' + str(user_id), date)
        day_expenses = await self.query_execute(query, select=True)
        output = ''
        for expense in range(len(day_expenses)):
            # print(expense)
            output += day_expenses[expense]['category'] + ' ' + \
                      day_expenses[expense]['merchandise'] + ' ' + \
                      str(day_expenses[expense]['price']) + ' ' + '\n'
        return output

    async def delete_expense(self, expense_id, user_id):
        query = 'DELETE FROM {0} WHERE Id=(''\'{1}\')'.format(
            'expenses' + str(user_id), expense_id)
        await self.query_execute(query)

    async def get_report(self, user_id):
        qeury = 'SELECT * FROM {0}'.format('expenses' + str(user_id))
        report = await self.query_execute(qeury, select=True)
        #print(report)
        return report


if __name__ == '__main__':
    open = Postgres_Query()
    # asyncio.get_event_loop().run_until_complete(open.open_connect())
    # asyncio.get_event_loop().run_until_complete(open.create_user_category(
    #   user_id=12345, category='PENIS'))
    asyncio.get_event_loop().run_until_complete(open.select_user_categories(
        302626122))

    # asyncio.get_event_loop().run_until_complete(open.add_user_expense(
    # user_id=16932, category='MOMM', goods='TITS', price=1.24,
    # date=datetime.datetime.now().date()))

    asyncio.get_event_loop().run_until_complete(open.get_last_five(302626122))
