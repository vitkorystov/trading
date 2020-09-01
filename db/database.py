import os
import psycopg2
from psycopg2 import extras


class DataBase:
    def __init__(self):
        db_host = os.getenv('DB_HOST', default='')
        db_port = os.getenv('DB_PORT', default=5432)
        db_name = os.getenv('DB_DATABASE', default='')
        db_user = os.getenv('DB_USER', default='')
        db_pass = os.getenv('DB_PASS', default='')
        self.conn = psycopg2.connect(f"dbname='{db_name}' user='{db_user}' host='{db_host}' password='{db_pass}'")

    def insert(self, data_list, table, ticker):
        cur = self.conn.cursor()
        for i, row in enumerate(data_list):
            print(i, row)
            sql_query = f"INSERT INTO {table} (ticker, date, open, high, low, close, volume) " \
                        f"VALUES " \
                        f"(\'{ticker}\', \'{row['date']}\', {row['open']}, {row['high']}, " \
                        f"{row['low']}, {row['close']}, {row['vol']})"
            cur.execute(sql_query)
            self.conn.commit()
            print('inserted..')
        cur.close()

    def get_fetch_all(self, query):
        cur = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        return res

    def __del__(self):
        self.conn.close()
