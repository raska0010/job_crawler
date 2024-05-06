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
    select
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

    def __init__(self):
        
        url_object = URL.create(
            "postgresql+psycopg2",
            username="postgres",
            password=dotenv_values('.env')['password'],  
            host="localhost",
            database="culture_jobs"
        )   
        self.engine = create_engine(url_object)

    def db_connection(self, max_retries=5, delay_seconds=5):
        retries = 0
        while retries < max_retries:
            try:
                self.engine.connect()
                return True
            except exc.OperationalError as e:
                print(f'Error connecting to Postgres: {e}\n')
                retries += 1
                print(f'Retrying in {delay_seconds} seconds... (Atempt {retries}/{max_retries})\n')
                time.sleep(delay_seconds)
        return False
    
    def table_exist(self):
        ins = inspect(self.engine)
        return self.table_name in ins.get_table_names()
    
    def create_table(self):
        if not self.db_connection():  # Is this right?
            raise ConnectionError('Could not connect to database')

        if not self.table_exist():
            self.metadata_obj.create_all(self.engine)

    def insert_data(self, data, table=ads_table):
        with self.engine.connect() as conn:
            conn.execute(
                insert(table).on_conflict_do_nothing(index_elements=['ad_url']),
                data
            )
            conn.commit()

    def get_new_entries(self, entry_date):
        stmt = select(self.ads_table).where(self.ads_table.c.date == entry_date)
        with self.engine.connect() as conn:
            for row in conn.execute(stmt):
                print(row)

    def drop_table(self):
        self.ads_table.drop(self.engine)
