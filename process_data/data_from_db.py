from db.database import DataBase


class DataFromDataBase(DataBase):

    def daily(self, ticker):
        sql_query = """
                   SELECT day_date AS date,
                          open_row.open AS open,
                          close_row.close AS close,
                          other_data_row.high AS high,
                          other_data_row.low AS low,
                          other_data_row.volume AS volume
                   FROM (SELECT DISTINCT date::date as day_date
                             FROM futures
                         WHERE ticker='{ticker}'
                         ) AS f,
                         LATERAL (SELECT date,
                                         open
                                  FROM futures
                                      WHERE date::date=f.day_date-1 AND EXTRACT(HOUR FROM date)=19 AND ticker='{ticker}'
                                  ORDER BY date LIMIT 1
                                  ) AS open_row,
                         LATERAL (SELECT date,
                                         close
                                  FROM futures
                                      WHERE date::date=f.day_date AND EXTRACT(HOUR FROM date)=18 AND ticker='{ticker}'
                                  ORDER BY date DESC LIMIT 1
                                  ) AS close_row,
                         LATERAL (SELECT max(high) AS high,
                                         min(low) AS low,
                                         sum(volume) as volume
                                  FROM futures
                                      WHERE date>=open_row.date AND date<=close_row.date AND ticker='{ticker}'
                                  ) AS other_data_row
                   ORDER BY day_date DESC;""".format(ticker=ticker)
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
                          FROM futures
                      WHERE ticker='{ticker}'
                          GROUP BY date_trunc('hour', date)
                      ORDER BY date_trunc('hour', date) DESC
                      ) AS f,
                      LATERAL (SELECT date,
                                      open
                               FROM futures
                                   WHERE date>=f.hour_date+interval '1 minute'
                                   AND ticker='{ticker}'
                               ORDER BY date LIMIT 1
                               ) AS open_row,
                      LATERAL (SELECT date,
                                      close
                               FROM futures
                                   WHERE date<=f.hour_date+interval '1 hour'
                                   AND ticker='{ticker}'
                               ORDER BY date DESC LIMIT 1
                               ) AS close_row,
                      LATERAL (SELECT max(high) AS high,
                                      min(low) AS low,
                                      sum(volume) as volume
                               FROM futures
                                   WHERE date>=open_row.date AND date<=close_row.date AND ticker='{ticker}'
                              ) AS other_data_row
                ORDER BY hour_date DESC;""".format(ticker=ticker)
        return self.get_fetch_all(query=sql_query)

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
                        FROM futures
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
                --other 
                LATERAL (SELECT max(high) AS high,
                                min(low) AS low,
                                sum(volume) as volume
                         FROM futures
                             WHERE date>=open_row.date AND date<=close_row.date AND ticker='{ticker}'
                         ) AS other_data_row
                ORDER BY date_generator.s_date DESC""".format(ticker=ticker, n=n)
        return self.get_fetch_all(query=sql_query)


'''
db = DataFromDataBase()
# r = db.minute(n=1, ticker='Si-9.20')
# r = db.hourly(ticker='Si-9.20')
r = db.daily(ticker='Si-9.20')

print(r[0])
print(r[1])
print(r[2])
'''