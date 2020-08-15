from data_from_file import DataFromFile
from strategy import Strategy
from indicators import Indicators

file = 'futures/SPFB.Si-9.20_200814_200814.csv'

data = DataFromFile(file=file)
# print(data.data_list[:50])

ind = Indicators(data=data.data_list)
ema_3 = ind.ema(n=3)


