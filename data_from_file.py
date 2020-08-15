import pandas as pd
from datetime import datetime


class DataFromFile:
    def __init__(self, file):
        self.file = file
        self.df = pd.read_csv(file, sep=';')
        self.data_list = []
        self.prepare_data()

    def prepare_data(self):
        for i, row in self.df.iterrows():
            data_row = {'index': i,
                        'date': datetime.strptime(row['<DATE>'] + ' ' + row['<TIME>'], '%d/%m/%y %H:%M:%S'),
                        'open': row['<OPEN>'],
                        'close': row['<CLOSE>'],
                        'high': row['<HIGH>'],
                        'low': row['<LOW>'],
                        'vol': row['<VOL>']
                        }
            self.data_list.append(data_row)
