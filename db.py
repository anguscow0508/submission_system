
import psycopg
from psycopg.rows import dict_row
import os


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="submissionn_db",
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        row_factory=dict_row
    )
