from db.database import DataBase
from psycopg2 import sql


class DataSupplier(DataBase):
    def __init__(self, table):
        super().__init__()
        self.table = table

    def _1m(self, ticker):
        sql_query = sql.SQL(""" 
                SELECT 
                    date, 
                    open, 
                    high, 
                    low, 
                    close, 
                    volume
                FROM {table_name}
                WHERE ticker=(SELECT id FROM tickers WHERE full_name={ticker_full_name})   
                ORDER BY date                 
                """).format(table_name=sql.Identifier(self.table), ticker_full_name=sql.Literal(ticker))

        return self.get_fetch_all(query=sql_query)

    def get_data(self, ticker):
        res = self._1m(ticker=ticker)
        print(res)
        if res is not None:
            keys = ['index', 'date', 'open', 'close', 'high', 'low', 'volume']
            data_dict = {key: [] for key in keys}
            for i, row in enumerate(res):
                for key in keys:
                    value = i if key == 'index' else row[key.lower()]
                    data_dict[key].append(value)
                '''
                data_row = {'index': i,
                            'date': row['date'],
                            'open': row['open'],
                            'close': row['close'],
                            'high': row['high'],
                            'low': row['low'],
                            'vol': row['volume']
                            }
                data_list.append(data_row)            
                print(data_row)
                '''
            # print(data_dict)
            return data_dict



