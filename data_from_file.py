import pandas as pd


class DataFromFile:
    def __init__(self, file):
        self.file = file
        self.df = pd.read_csv(file, sep=';')
        self.data_list = []
        self.prepare_data()

    def prepare_data(self):
        for i, row in self.df.iterrows():
            data_row = {'open': row['<OPEN>'],
                        'close': row['<OPEN>'],
                        'high': row['<CLOSE>'],
                        'low': row['<LOW>'],
                        'vol': row['<VOL>']
                        }
            self.data_list.append(data_row)
