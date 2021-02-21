import pandas as pd
from db.insert_db import InsertDb
from process_data.data_from_file import DataFromFile


file = 'futures_csv/1min/SPFB.SBRF-12.20_200901_201217.csv'
df = pd.read_csv(file, sep=';')


data_from_file = DataFromFile(file=file)
data_list = data_from_file.data_list

d_base = InsertDb()
d_base.insert_from_csv(data=data_list, table='futures', ticker='SBRF-12.20', timeframe='1m')
