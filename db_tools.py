from dotenv import dotenv_values
from sqlalchemy import (
    URL,
    create_engine,
    exc
)
import subprocess
import time


url_object = URL.create(
    "postgresql+psycopg2",
    username="postgres",
    password=dotenv_values('.env')['password'],  
    host="localhost",
    database="culture_jobs",
)


engine = create_engine(url_object)


# Test for connection to postgres 
def test_db_connection(engine, max_retries=5, delay_seconds=5):
    retries = 0
    while retries < max_retries:
        try:
            engine.connect()
            return True
        except exc.OperationalError as e:
            print(f'Error connection to Postgres: {e}\n')
            retries += 1
            print(f'Retrying in {delay_seconds} seconds... (Atempt {retries}/{max_retries})\n')
            time.sleep(delay_seconds)
    print('Max retries reached. Exiting...')
    return False


if not test_db_connection(engine=engine):
    exit(1)