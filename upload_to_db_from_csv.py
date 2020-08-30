import pandas as pd

file = 'futures/1min/SPFB.Si-9.20_200615_200821.csv'
df = pd.read_csv(file, sep=';')



print(df.head())

