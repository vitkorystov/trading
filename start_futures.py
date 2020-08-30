from data_from_file import DataFromFile
from strategy_with_2ma import StrategyWithMA
from indicators import Indicators
import glob
import mplfinance as mpf



file_list = [file for file in glob.glob("futures/1min/*.csv") if 'Si-9.20' in file]

file = file_list[0]
print(file)
data_from_file = DataFromFile(file=file)
data = data_from_file.data_list

df = data_from_file.df
#df.columns = ['ticker', 'per', 'Date', 'Time',  'Open', 'High', 'Low', 'Close', 'Volume']
#print(df.head())

df1 = df.rename(columns={'<DATE>': 'Date',
                                       '<OPEN>': 'Open',
                                       '<HIGH>': 'High',
                                       '<LOW>': 'Low',
                                       '<CLOSE>': 'Close',
                                       '<VOL>': 'Volume',
                                       })


print(df1.head())


'''
for file in file_list:
    data_from_file = DataFromFile(file=file)
    data = data_from_file.data_list            
    my_indicators = Indicators(data=data)
    n_long = 10
    n_short = 2
    ma_long = my_indicators.ema(n=n_long)
    ma_short = my_indicators.ema(n=n_short)

    strategy_ma = StrategyWithMA(data=data,
                                 start_index=(n_long+n_short+1),
                                 take_profit_range=150,
                                 stop_loss_range=10,
                                 delta_limit=100)

    strategy_ma.set_ma(ma_short=ma_short, ma_long=ma_long)
    strategy_ma.is_print = False
    strategy_ma.deal_commission = 2.13
    strategy_ma.run()

    print(strategy_ma.stats)


'''
