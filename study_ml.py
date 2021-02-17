from process_data.data_from_file import DataFromFile
import datetime
from dataclasses import dataclass
import glob
from tech_analysis.candles import Candles



"""
Исследуем свечные модели: бычье и медвежье поглощения
"""

files = glob.glob("futures_csv/1min/*.csv")
file = "futures_csv/1min/SPFB.Si-3.21_201201_210216.csv"


dff = DataFromFile(file=file)
data = dff.data_list

print(dff.ticker)

'''
for row in data:
    target = Candles(open=row['open'], close=row['close'], high=row['high'], low=row['low'])

    print(row['open'], row['close'], target.is_bear(), target.is_bull(), target.is_dodge())
'''







