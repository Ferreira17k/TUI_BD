import psycopg2
from psycopg2.extensions import connection as PGConnection

def get_connection() -> PGConnection:
    return psycopg2.connect(
        dbname="sql_mystery",
        user="tui",
        password="504",
        host="10.61.49.169",
        port="5432"
    )
