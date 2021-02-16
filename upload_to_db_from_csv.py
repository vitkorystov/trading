import pandas as pd
from db.database import DataBase
from process_data.data_from_file import DataFromFile


file = 'futures_csv/1min/SPFB.Si-9.20_200831_200902.csv'
df = pd.read_csv(file, sep=';')

d_base = DataBase()
data_from_file = DataFromFile(file=file)
data_list = data_from_file.data_list

# d_base.insert(data_list=data_list, table='futures_csv', ticker='Si-9.20')


