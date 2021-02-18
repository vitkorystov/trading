from db.database import DataBase


class DataFromDataBase(DataBase):

    def daily(self, ticker):
        sql_query = """
                   WITH previous_dates AS (
                       SELECT day_date, 
                               LAG (day_date, 1) OVER (ORDER BY day_date) AS previous_date
                       FROM (
                           SELECT DISTINCT date::date as day_date
                               FROM futures_csv
                           WHERE ticker='{ticker}'
                           ORDER BY day_date DESC) AS f 
                   ), 
        
                   final_res AS (
                       SELECT day_date::timestamp AS date,
                              open_row.open AS open,
                              close_row.close AS close,
                              other_data_row.high AS high,
                              other_data_row.low AS low,
                              other_data_row.volume AS volume
                       FROM (SELECT DISTINCT date::date as day_date
                                 FROM futures_csv
                             WHERE ticker='{ticker}'
                             ) AS f,
                             LATERAL (SELECT date,
                                             open
                                      FROM futures_csv
                                          WHERE date::date=(SELECT previous_date 
                                                                FROM previous_dates 
                                                            WHERE day_date=f.day_date)
                                                AND EXTRACT(HOUR FROM date)=19 AND ticker='{ticker}'
                                      ORDER BY date LIMIT 1
                                      ) AS open_row,
                             LATERAL (SELECT date,
                                             close
                                      FROM futures_csv
                                          WHERE date::date=f.day_date AND EXTRACT(HOUR FROM date)=18 AND ticker='{ticker}'
                                      ORDER BY date DESC LIMIT 1
                                      ) AS close_row,
                             LATERAL (SELECT max(high) AS high,
                                             min(low) AS low,
                                             sum(volume) as volume
                                      FROM futures_csv
                                          WHERE date>=open_row.date AND date<=close_row.date AND ticker='{ticker}'
                                      ) AS other_data_row
                       ORDER BY day_date
                   ) 
                   SELECT * FROM final_res;""".format(ticker=ticker)
        return self.get_fetch_all(query=sql_query)

    def hourly(self, ticker):
        sql_query = """
                SELECT hour_date AS date,
                       open_row.open AS open,
                       close_row.close AS close,
                       other_data_row.high AS high,
                       other_data_row.low AS low,
                       other_data_row.volume AS volume
                FROM (SELECT date_trunc('hour', date) as hour_date
                          FROM futures_csv
                      WHERE ticker='{ticker}'
                          GROUP BY date_trunc('hour', date)
                      ORDER BY date_trunc('hour', date) DESC
                      ) AS f,
                      LATERAL (SELECT date,
                                      open
                               FROM futures_csv
                                   WHERE date>=f.hour_date+interval '1 minute'
                                   AND ticker='{ticker}'
                               ORDER BY date LIMIT 1
                               ) AS open_row,
                      LATERAL (SELECT date,
                                      close
                               FROM futures_csv
                                   WHERE date<=f.hour_date+interval '1 hour'
                                   AND ticker='{ticker}'
                               ORDER BY date DESC LIMIT 1
                               ) AS close_row,
                      LATERAL (SELECT max(high) AS high,
                                      min(low) AS low,
                                      sum(volume) as volume
                               FROM futures_csv
                                   WHERE date>=open_row.date AND date<=close_row.date AND ticker='{ticker}'
                              ) AS other_data_row
                ORDER BY hour_date;""".format(ticker=ticker)
        return self.get_fetch_all(query=sql_query)

    # n - число минут, по условию -> 60%n=0 (n=1,2,3,4,5,6,10,12,15,20,30)
    def minute(self, n, ticker):
        sql_query = """
                SELECT
                    date_generator.s_date AS date, 
                    open_row.open AS open, 
                    close_row.close AS close, 
                    other_data_row.high AS high, 
                    other_data_row.low AS low, 
                    other_data_row.volume AS volume	
                FROM (SELECT date_trunc('hour', date) as hour_date
                          FROM futures
                      WHERE ticker='{ticker}'
                          GROUP BY date_trunc('hour', date)
                      ORDER BY date_trunc('hour', date) DESC
                      ) as f
                CROSS JOIN LATERAL (	
                SELECT s_date FROM generate_series(hour_date,
                                              hour_date::timestamp + interval '1 hour'-interval '{n} minutes',
                                              '{n} minutes') as s_date) as date_generator,
                -- open	
                LATERAL (SELECT date,
                                open
                        FROM futures_csv
                           WHERE date=date_generator.s_date+interval '1 minute' AND ticker='{ticker}'
                        ORDER BY date LIMIT 1
                        ) AS open_row,
                -- close		
                LATERAL (SELECT date,
                                close
                        FROM futures
                           WHERE date=date_generator.s_date+interval '{n} minutes' AND ticker='{ticker}'
                        ORDER BY date LIMIT 1
                        ) AS close_row,
                -- other 
                LATERAL (SELECT max(high) AS high,
                                min(low) AS low,
                                sum(volume) as volume
                         FROM futures
                             WHERE date>=open_row.date AND date<=close_row.date AND ticker='{ticker}'
                         ) AS other_data_row
                ORDER BY date_generator.s_date""".format(ticker=ticker, n=n)
        return self.get_fetch_all(query=sql_query)

    def get_data(self, period, ticker, n=1):
        if period == 'daily':
            res = self.daily(ticker=ticker)
        elif period == 'hourly':
            res = self.hourly(ticker=ticker)
        else:
            res = self.minute(ticker=ticker, n=n)
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


            '''
            import pandas as pd
            keys = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
            df = pd.DataFrame(data_dict,
                              columns=keys)
            df.set_index('Date', inplace=True)
            print(df.head(3))
            print(df.tail(3))
            import mplfinance as mpf
            mpf.plot(df, type='candle')
            '''

# db = DataFromDataBase()
# r = db.minute(n=1, ticker='Si-9.20')
# r = db.hourly(ticker='Si-9.20')
# print(r[0])
# print(r[1])
# print(r[2])

# db.get_data(ticker='Si-9.20', period='daily')
