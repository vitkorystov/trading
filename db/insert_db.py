from db.database import DataBase
from process_data.data_from_file import DataFromFile
from psycopg2 import sql
from psycopg2.extras import execute_values
from logger import Logger


class InsertDb(DataBase):
    def __init__(self):
        super().__init__()
        self.logger = Logger('insertDb').logger

    def insert_from_csv(self, data, table, ticker, timeframe):
        cur = self.conn.cursor()

        try:
            # ticker id
            query_ticker = sql.SQL("SELECT id FROM tickers WHERE full_name=%s;")
            cur.execute(query_ticker, (ticker,))
            ticker_id = cur.fetchone()
            if ticker_id is None:
                raise Exception('No ticker id was found!')
            else:
                ticker_id = ticker_id[0]

            # timeframe id
            query_timeframe = sql.SQL("SELECT id FROM timeframes WHERE timeframe=%s;")
            cur.execute(query_timeframe, (timeframe,))
            timeframe_id = cur.fetchone()
            if timeframe_id is None:
                raise Exception('No timeframe id was found!')
            else:
                timeframe_id = timeframe_id[0]

            # подготовка данных
            prepared_data = list(map(lambda x: (ticker_id, timeframe_id, x['date'],
                                                x['open'], x['high'], x['low'], x['close'], x['vol']), data))

            self.logger.info(f'Prepared {len(prepared_data)} rows...')

            # основной запрос
            query = sql.SQL("""INSERT INTO {table_name} 
                            (ticker, timeframe, date, open, high, low, close, volume) VALUES %s 
                            ON CONFLICT (ticker, timeframe, date) DO NOTHING;                          
                            """).format(table_name=sql.Identifier(table))

            execute_values(cur, query, prepared_data)

            self.conn.commit()

            self.logger.info('Inserted successfully!')

        except Exception as ex:
            self.logger.exception(f'insert_from_csv error: {ex}')

        cur.close()

