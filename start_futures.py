from process_data.data_from_file import DataFromFile
from process_data.data_from_db import DataFromDataBase
from tech_analysis.indicators import Indicators
from strategies.strategy_with_2ma import StrategyWith2MA

# data_db = DataFromDataBase()
data_dict = DataFromDataBase().get_data(period='hourly', ticker='Si-9.20')

# индикаторы
my_indicators = Indicators(data=data_dict)
n_long = 5
n_short = 2
ma_long = my_indicators.ema(n=n_long)
ma_short = my_indicators.sma(n=n_short)

# стратегия с 2 МА
strategy_ma = StrategyWith2MA(data=data_dict,
                              start_index=(n_long+n_short+1),
                              take_profit_range=300,
                              stop_loss_range=300,
                              delta_limit=300)

strategy_ma.set_ma(ma_short=ma_short, ma_long=ma_long)
strategy_ma.is_print = True
strategy_ma.deal_commission = 2.13
strategy_ma.run()

print(strategy_ma.stats)






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
