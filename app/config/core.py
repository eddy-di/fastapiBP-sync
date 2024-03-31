import os

from dotenv import load_dotenv

load_dotenv()


BP_DB_USER = os.environ.get('BP_DB_USER')
BP_DB_PASS = os.environ.get('BP_DB_PASS')
BP_DB_HOST = os.environ.get('BP_DB_HOST')
BP_DB_NAME = os.environ.get('BP_DB_NAME')
BP_DB_PORT = os.environ.get('BP_DB_PORT')

database_url = (
    f'postgresql://{BP_DB_USER}:{BP_DB_PASS}'
    f'@{BP_DB_HOST}:{BP_DB_PORT}/{BP_DB_NAME}'
)
