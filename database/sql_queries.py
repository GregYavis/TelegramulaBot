from database.config import DatabaseConfig

class SqlQueries(DatabaseConfig):

    @staticmethod
    def create_database(db_name: str):
        return f'CREATE DATABASE IF NOT EXISTS {db_name};'

    @staticmethod
    def ct_users(db_name: str):
        return f"USE {db_name}; " \
               f"CREATE TABLE IF NOT EXISTS users (" \
               f"user_id INT NOT NULL, " \
               f"balance FLOAT, " \
               f"UNIQUE (user_id))"

    @staticmethod
    def ct_categories(db_name: str):
        return f"USE {db_name};" \
               "CREATE TABLE IF NOT EXISTS categories (" \
               "category VARCHAR(150), " \
               "user_id INT, " \
               "FOREIGN KEY (user_id) REFERENCES users (user_id))"

    @staticmethod
    def ct_expenses(db_name: str):
        return f"USE {db_name};" \
               "CREATE TABLE IF NOT EXISTS expenses (" \
               "category VARCHAR(150), " \
               "user_id INT, " \
               "FOREIGN KEY (user_id) REFERENCES bot_backend.users (user_id))"

    @staticmethod
    def drop_database(db_name: str):
        return f'DROP DATABASE IF EXISTS {db_name};'

    @staticmethod
    def select_categories(self, user_id):
        return f'USE {self.backend_db_name};' \
               f'SELECT categories FROM categories WHERE user_id = {user_id};'

    @staticmethod
    def create_category(category: str, user_id: int):
        return f'INSERT INTO categories (category, user_id) VALUES {category}, {user_id}'