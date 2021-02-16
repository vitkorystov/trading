from process_data.data_from_file import DataFromFile
import datetime
from dataclasses import dataclass
import glob
from tech_analysis.candles import Candles


"""
Исследуем свечные модели: бычье и медвежье поглощения
"""

files = glob.glob("futures_csv/1min/*.csv")


for file in files:

    dff = DataFromFile(file=file)
    data = dff.data_list

    for row in data:
        target = Candles(open=row['open'], close=row['close'], high=row['high'], low=row['low'])

        print(row['open'], row['close'], target.is_bear(), target.is_bull(), target.is_dodge())

    break






