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

    def __del__(self):
        self.conn.close()

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

    # определить, что сработает раньше - стоп-лосс или тейк-профит
    # если они близки, а также если основной тайм-фрейм велик, например час/день.
    def who_1st_stop_loss_or_take_profit(self, ticker,
                                         date_from, date_to,
                                         high, low):
        sql_query = """
                       SELECT 
                            date, 
                            'low' as target
                       FROM 
                       (SELECT 
                           date
                       FROM futures
                           WHERE date  BETWEEN '{date_from}' AND '{date_to}'
                               AND low<={low} 
                               AND ticker='{ticker}'
                       ORDER BY date ASC LIMIT 1
                       ) as t1
                       UNION ALL
                       SELECT 
                           date, 
                           'high' as target 
                       FROM 	
                       (SELECT 
                           date
                       FROM futures
                           WHERE date BETWEEN '{date_from}' AND '{date_to}'
                               AND high>={high} 
                               AND ticker='{ticker}' 
                       ORDER BY date ASC LIMIT 1
                       ) AS t2
                    """.format(date_from=date_from, date_to=date_to,
                               high=high, low=low, ticker=ticker)

        return self.get_fetch_all(query=sql_query)

'''
from datetime import datetime
db = DataBase()
db.who_1st_stop_loss_or_take_profit(ticker='Si-9.20', deal_type='buy',
                                    date_from=datetime(2020, 9, 2, 17, 1),
                                    date_to=datetime(2020, 9, 2, 18, 0),
                                    take_profit=75727, stop_loss=75194
                                    )
'''