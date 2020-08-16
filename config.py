import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
administrator_id = os.getenv('ADMINISTRATOR')
db_name = 'FN4D'
db_init = 'FN4D_INIT'