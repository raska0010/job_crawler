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
    # insert
)
from sqlalchemy.dialects.postgresql import insert
import subprocess
import time
import json
from datetime import date

# url_object = URL.create(
# "postgresql+psycopg2",
# username="postgres",
# password=dotenv_values('.env')['password'],  
# host="localhost",
# database="culture_jobs",
# )

# engine = create_engine(url_object)


class DbTools:
    url_object = URL.create(
    "postgresql+psycopg2",
    username="postgres",
    password=dotenv_values('.env')['password'],  
    host="localhost",
    database="culture_jobs",
    )   

    engine = create_engine(url_object)

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

    def db_connection(self, engine=engine, max_retries=5, delay_seconds=5):
        retries = 0
        while retries < max_retries:
            try:
                engine.connect()
                return True
            except exc.OperationalError as e:
                print(f'Error connecting to Postgres: {e}\n')
                retries += 1
                print(f'Retrying in {delay_seconds} seconds... (Atempt {retries}/{max_retries})\n')
                time.sleep(delay_seconds)
        return False
    
    def table_exist(self, engine=engine):
        ins = inspect(engine)
        return self.table_name in ins.get_table_names()
    
    def create_table(self, engine=engine):
        if not self.db_connection(self.engine):  # Is this right?
            raise ConnectionError('Could not connect to database')

        if not self.table_exist(engine):
            self.metadata_obj.create_all(engine)

    def insert_data(self, data, table=ads_table, engine=engine):
        with engine.connect() as conn:
            result = conn.execute(
                insert(table).on_conflict_do_nothing(index_elements=['ad_url']),
                data
            )
            conn.commit()
