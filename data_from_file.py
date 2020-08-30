import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class DataLists:
    open: list
    high: list
    low: list
    close: list
    index: list
    date: list



class DataFromFile:
    def __init__(self, file):
        self.file = file
        self.df = pd.read_csv(file, sep=';')
        self.data_list = []
        # self.prepare_data()

    def prepare_data(self):


        for i, row in self.df.iterrows():
            # -1 мин для синхронизации с графиком на ru.tradingview.com
            row_date = datetime.strptime(row['<DATE>']+' '+row['<TIME>'], '%d/%m/%y %H:%M:%S')  #-timedelta(seconds=60)
            data_row = {'index': i,
                        'date': row_date,
                        'open': row['<OPEN>'],
                        'close': row['<CLOSE>'],
                        'high': row['<HIGH>'],
                        'low': row['<LOW>'],
                        'vol': row['<VOL>']
                        }
            self.data_list.append(data_row)
