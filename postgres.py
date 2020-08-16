import asyncio
import asyncpg
import pyexcel


class PostgresQuery:
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
        if not await self.select_user_categories(user_id):
            self.query = 'CREATE TABLE IF NOT EXISTS "{0}" ' \
                         '(category VARCHAR (50));' \
                         'INSERT INTO "{0}" (category) VALUES (''\'{1}\');' \
                         'INSERT INTO "{0}" (category) VALUES (''\'{2}\');'. \
                format('categories' + str(user_id), category, 'Баланс')
            await self.query_execute(self.query)
        else:
            self.query = 'CREATE TABLE IF NOT EXISTS "{0}" ' \
                         '(category VARCHAR (50));' \
                         'INSERT INTO "{0}" (category) VALUES (''\'{1}\')'. \
                format('categories' + str(user_id), category)
            await self.query_execute(self.query)

    async def select_user_categories(self, user_id: int):
        self.query = 'SELECT * FROM {0}'.format('categories' + str(user_id))
        try:
            result = await self.query_execute(query_string=self.query,
                                              select=True)

            self.user_categories = [category[0] for category in result]
            return self.user_categories
        except asyncpg.exceptions.UndefinedTableError:
            return False  # return to check that user's table doesn't exists

    async def register_user(self, user_id):
        self.query = 'CREATE TABLE IF NOT EXISTS BotUsers ' \
                     '(user_id INT);' \
                     'INSERT INTO BotUsers VALUES (''\'{0}\');'.format(user_id)
        await self.query_execute(self.query)

    async def get_users(self):
        self.query = 'SELECT * FROM BotUsers;'
        users_id = await self.query_execute(self.query, select=True)
        users_list = [user[0] for user in users_id]
        return users_list

    async def delete_user_category(self, user_id: int, category):
        self.query = 'DELETE FROM {0} WHERE category=(''\'{1}\')'.format(
            'categories' + str(user_id), category)
        await self.query_execute(self.query)

    async def init_balance(self, user_id, balance):
        self.query = 'CREATE TABLE IF NOT EXISTS "{0}" ' \
                     '(Id SERIAL,' \
                     'category VARCHAR (100),' \
                     'merchandise VARCHAR (100),' \
                     'price FLOAT NOT NULL,' \
                     'balance FLOAT, ' \
                     'date_create date);' \
                     'INSERT INTO "{0}" (price, balance)' \
                     'VALUES (0, ''\'{1}\')'. \
            format('expenses' + str(user_id), float(balance))
        await self.query_execute(self.query)

    async def update_balance(self, user_id, update):
        current_balance = await self.get_balance(user_id)
        self.query = 'INSERT INTO "{0}" (price, balance)' \
                     'VALUES (0, ''\'{1}\')'. \
            format('expenses' + str(user_id),
                   float(current_balance) + float(update))
        await self.query_execute(self.query)

    async def get_balance(self, user_id):
        self.query = 'SELECT balance FROM "{0}" ORDER BY Id DESC LIMIT 1'.format(
            'expenses' + str(user_id))
        try:
            self.balance = await self.query_execute(self.query, select=True)
            return self.balance[0]['balance']
        except asyncpg.exceptions.UndefinedTableError:
            return False

    async def add_user_expense(self, expense_data):
        # user_id, category, goods, price, date = expense_data
        # вытащить текущий баланс
        current_balance = await self.get_balance(
            user_id=expense_data['user_id'])
        self.query = 'CREATE TABLE IF NOT EXISTS "{0}" ' \
                     '(Id SERIAL,' \
                     'category VARCHAR (100),' \
                     'merchandise VARCHAR (100),' \
                     'price FLOAT NOT NULL,' \
                     'balance FLOAT,' \
                     'date_create date);' \
                     'INSERT INTO "{0}" ' \
                     'VALUES (' \
                     'DEFAULT,''\'{1}\',''\'{2}\',''\'{3}\',''\'{4}\',''\'{5}\')'. \
            format('expenses' + str(expense_data['user_id']),
                   expense_data['category'],
                   expense_data['merchandise'],
                   expense_data['price'],
                   current_balance - expense_data['price'],
                   expense_data['date'])
        await self.query_execute(self.query)

    async def get_last_five(self, user_id):
        self.query = 'SELECT * FROM {0} WHERE ' \
                     'category!=(''\'Balance\') ORDER BY Id DESC LIMIT 5 '. \
            format('expenses' + str(user_id))
        try:
            last_five = await self.query_execute(query_string=self.query,
                                                 select=True)
            self.output = {}
            for expense in range(len(last_five)):
                self.output[str(expense)] = {
                    'expense_id': last_five[expense]['id'],
                    'category': last_five[expense]['category'],
                    'merchandise': last_five[expense]['merchandise'],
                    'price': last_five[expense]['price'],
                    'date': last_five[expense]['date_create']}
            return self.output
        except asyncpg.exceptions.UndefinedTableError:
            return False

    async def get_day(self, user_id, date):
        self.query = 'SELECT * FROM {0} WHERE date_create = (''\'{1}\')'.format(
            'expenses' + str(user_id), date)
        try:
            self.day_expenses = await self.query_execute(self.query,
                                                         select=True)
            output = ''
            for expense in range(len(self.day_expenses)):
                # print(expense)
                output += self.day_expenses[expense]['category'] + ' ' + \
                          self.day_expenses[expense]['merchandise'] + ' ' + \
                          str(self.day_expenses[expense]['price']) + ' ' + '\n'
            return output
        except asyncpg.exceptions.UndefinedTableError:
            return False

    async def delete_expense(self, expense_id, user_id):
        self.query = 'DELETE FROM {0} WHERE Id=(''\'{1}\')'.format(
            'expenses' + str(user_id), expense_id)
        await self.query_execute(self.query)

    async def get_report(self, user_id):
        self.qeury = 'SELECT * FROM "{0}" WHERE category IS NOT NULL'.format(
            'expenses' + str(user_id))
        output = []
        try:
            report = await self.query_execute(self.qeury, select=True)
            for expense in range(len(report)):
                output.append({
                    '1) Категория': report[expense]['category'],
                    '2) Товар/услуга': report[expense]['merchandise'],
                    '3) Цена': report[expense]['price'],
                    '4) Баланс': report[expense]['balance'],
                    '5) Дата': report[expense]['date_create']})
            pyexcel.save_as(
                records=output, dest_file_name='{0}.xls'.format(user_id))
            return True
        except asyncpg.exceptions.UndefinedTableError:
            return False


if __name__ == '__main__':
    open = PostgresQuery()
    # asyncio.get_event_loop().run_until_complete(open.open_connect())
    # asyncio.get_event_loop().run_until_complete(open.create_user_category(
    #   user_id=12345, category='PENIS'))
    # asyncio.get_event_loop().run_until_complete(open.select_user_categories(
    #   302626122))

    # asyncio.get_event_loop().run_until_complete(open.add_user_expense(
    # user_id=16932, category='MOMM', goods='TITS', price=1.24,
    # date=datetime.datetime.now().date()))

    asyncio.get_event_loop().run_until_complete(open.get_users())
# asyncio.get_event_loop().run_until_complete(open.select_user_categories(
# 302626122))
