from process_data.data_from_file import DataFromFile
import datetime

file = "futures/1min/SPFB.Si-6.20_200318_200619.csv"


dff = DataFromFile(file=file)

data = dff.data_list

print(data[:1])

direct_to_deal = 'buy'   # 'buy/sell'
current_date = None
for i, row in enumerate(data):
    date = row['date'].date()
    time = row['date'].time()
    _open = row['open']
    _close = row['close']

    if i == 0:
        current_date = date

    if date == current_date:
        if datetime.time(hour=10, minute=30, second=0) < time < datetime.time(hour=10, minute=59, second=0):

            print(time, _close, _close%100)


    else:
        current_date = date
        print('new date!', row['date'])
        break



