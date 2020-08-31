import pandas as pd
from db.database import DataBase
from process_data.data_from_file import DataFromFile


file = 'futures/1min/SPFB.Si-6.20_200318_200619.csv'
df = pd.read_csv(file, sep=';')

d_base = DataBase()
data_from_file = DataFromFile(file=file)
data_list = data_from_file.data_list

# d_base.insert(data_list=data_list, table='futures', ticker='Si-6.20')


