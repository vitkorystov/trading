from process_data.data_from_file import DataFromFile
import datetime
from dataclasses import dataclass
import glob


"""
Исследуем свечные модели: бычье и медвежье поглощения
"""

files = glob.glob("futures_csv/1min/*.csv")


# parameters
long_body_size = 15


@dataclass
class Candles:
    open: float
    close: float

    def is_bull(self) -> bool:
        return self.close > self.open

    def is_bear(self) -> bool:
        return self.close < self.open

    def is_long_body(self) -> bool:
        return self.body() > long_body_size

    def body(self) -> float:
        return abs(self.open - self.close)


res = {'+': 0, '-': 0, 'all': 0}
bodies = {'pos': 0, 'neg': 0}

for file in files:
    # file = "futures_csv/5min/SPFB.Si-3.21_200601_210208.csv"
    dff = DataFromFile(file=file)
    data = dff.data_list

    print(file)

    for i, row in enumerate(data, 0):
        if 2 <= i < (len(data) - 1):
            date = row['date'].date()
            time = row['date'].time()
            # time = row['date'].time()
            target = Candles(open=data[i]['open'], close=data[i]['close'])
            deal = Candles(open=data[i+1]['open'], close=data[i+1]['close'])
            previous_1 = Candles(open=data[i-1]['open'], close=data[i-1]['close'])
            previous_2 = Candles(open=data[i-2]['open'], close=data[i-2]['close'])

            if previous_1.is_bull() and previous_2.is_bull() and target.is_bear() \
                    and previous_1.open > previous_2.open and previous_2.close < previous_1.close < target.open \
                    and previous_1.is_long_body() \
                    and target.body() > previous_1.body()*1:
                # print(date, time, deal.is_bear(), deal.body())

                if deal.is_bear():
                    bodies['pos'] += deal.body()
                    res['+'] += 1
                else:
                    bodies['neg'] += deal.body()
                    res['-'] += 1
                res['all'] += 1

    print(f"{bodies=}, {bodies['pos'] - bodies['neg']}")
    print(f"{res=} \n")







