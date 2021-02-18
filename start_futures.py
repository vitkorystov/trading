from process_data.data_from_file import DataFromFile
from process_data.data_from_db import DataFromDataBase
from tech_analysis.indicators import Indicators
from strategies.strategy_with_2ma import StrategyWith2MA

ticker = 'Si-9.20'

# data_db = DataFromDataBase()
data_dict = DataFromDataBase().get_data(period='hourly', ticker=ticker)

# индикаторы
my_indicators = Indicators(data=data_dict)
n_long = 3
n_short = 1
ma_long = my_indicators.ema(n=n_long)
ma_short = my_indicators.ema(n=n_short)

# стратегия с 2 МА
strategy_ma = StrategyWith2MA(data=data_dict,
                              start_index=(n_long+n_short+1),
                              take_profit=150,
                              stop_loss=10,
                              delta_limit=50,
                              main_time_frame='1hour',
                              ticker=ticker)

strategy_ma.set_ma(ma_short=ma_short, ma_long=ma_long)
strategy_ma.is_print = True
strategy_ma.deal_commission = 2.13
strategy_ma.run()

print(strategy_ma.stats)






