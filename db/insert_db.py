from db.database import DataBase


class InsertDb(DataBase):

    def insert_from_csv(self):
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