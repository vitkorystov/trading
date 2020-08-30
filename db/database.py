import os
import psycopg2


class DataBase:
    def __init__(self):
        db_host = os.getenv('DB_HOST', default='')
        db_port = os.getenv('DB_PORT', default=5432)
        db_name = os.getenv('DB_DATABASE', default='')
        db_user = os.getenv('DB_USER', default='')
        db_pass = os.getenv('DB_PASS', default='')
        self.conn = psycopg2.connect(f"dbname='{db_name}' user='{db_user}' host='{db_host}' password='{db_pass}'")

    def insert(self, df, table, ticker):
        cur = self.conn.cursor()


        cur.close()

    def __del__(self):
        self.conn.close()
