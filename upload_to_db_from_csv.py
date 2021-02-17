import pandas as pd
from db.insert_db import InsertDb
from process_data.data_from_file import DataFromFile


file = 'futures_csv/1min/SPFB.Si-3.21_210216_210217.csv'
df = pd.read_csv(file, sep=';')


data_from_file = DataFromFile(file=file)
data_list = data_from_file.data_list

d_base = InsertDb()
d_base.insert_from_csv(data=data_list, table='futures', ticker='Si-3.21', timeframe='1m')


