from dotenv import dotenv_values
from sqlalchemy import (
    URL,
    create_engine,
    exc,
    inspect,
    MetaData,
    Table,
    Column,
    BIGINT,
    Sequence,
    TEXT,
    VARCHAR,
    DATE,
    insert
)
import subprocess
import time
import json 


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


metadata_obj = MetaData()
table_name = 'job_ads'
ads_table = Table(
    table_name,
    metadata_obj,
    Column('id', BIGINT, Sequence('ad_id', start=1), primary_key=True),
    Column('job_description', TEXT, nullable=False ),
    Column('ad_url', TEXT, unique=True, nullable=False),
    Column('city', VARCHAR(50), nullable=False),  # Change to VARCHAR(4)
    Column('date', DATE, nullable=False)
)


# Test if table exist
def test_table_exist(engine, table_name):
    ins = inspect(engine)
    if table_name in ins.get_table_names():
        return True
    else:
        return False
    

if not test_table_exist(engine, table_name):
    metadata_obj.create_all(engine)


def insert_data(engine, data, table):
    with engine.connect() as conn:
        result = conn.execute(
            insert(table),
            data
        )
        conn.commit()




