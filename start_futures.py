from data_from_file import DataFromFile
from strategy_with_ma import StrategyWithMA
from indicators import Indicators

file = 'futures/SPFB.Si-9.20_200821_200821.csv'

data_from_file = DataFromFile(file=file)


my_indicators = Indicators(data=data_from_file.data_list)
ema_long = my_indicators.ema(n=100)
ema_short = my_indicators.ema(n=5)

strategy_ma = StrategyWithMA(data=data_from_file.data_list, start_index=110)
strategy_ma.set_ma(ma_short=ema_short, ma_long=ema_long)
strategy_ma.run()

print(strategy_ma.statistic)
