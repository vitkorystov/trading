from dataclasses import dataclass
from datetime import datetime, timedelta
from db.database import DataBase


# текущие параметры
@dataclass
class Price:
    index: int = 0
    date: datetime = None
    open: float = 0.0
    close: float = 0.0
    high: float = 0.0
    low: float = 0.0


# статистика
@dataclass
class Statistic:
    profit_deals: int = 0
    loss_deals: int = 0
    total_commission: float = 0
    bank: float = 0
    bank_with_comm: float = 0


class Strategy:
    def __init__(self, data, start_index, take_profit, stop_loss, main_time_frame, ticker):
        self.data = data
        self.ticker = ticker
        self.start_index = start_index
        self.end_deal_price = None      # цена завершения сделки
        self.stats = Statistic()
        self.price = Price()
        # ----------------- параметры -------------------------
        self.is_print = True
        self.deal_commission = 0
        # значение тейк-профита и стоп-лосса, в пунктах
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        # если сделка завершилась, но нужно сразу открыть новую
        self.is_open_new_after_closing = True
        # основной тайм-фрейм
        self.main_time_frame = main_time_frame

        # database
        self.db = DataBase()

    # условие старта сделки --> покупки/продажи
    # is_buy -> True=buy, False=sell
    def is_start_deal(self, *args, **kwargs):
        pass

    # условие по тейк-профиту - возвращает True/False
    def is_take_profit(self, *args, **kwargs):
        pass

    # условие по стоп-лоссу - возвращает True/False
    def is_stop_loss(self, *args, **kwargs):
        pass

    # условие завершения сделки (помимо достижения тейк-профита или стоп-лосса)
    def is_end_deal(self, *args, **kwargs):
        pass

    def print_end_deal(self, deal_type, deal_res, profit, price, date):
        if self.is_print:
            print(f'finish-->  deal_type: {deal_type}, closed by: {deal_res}, profit={profit} \n'
                  f'{price}, date: {date} \n')

    def print_start_deal(self, deal_type, start_price, date, take_profit_price, stop_loss_price):
        if self.is_print:
            print(f'start-->  deal_type: {deal_type}, start_price={start_price},  date: {date} \n'
                  f'take_profit_price={take_profit_price}, stop_loss_price={stop_loss_price}')

    def add_stat(self, profit):
        if profit >= 0:
            self.stats.profit_deals += 1
        else:
            self.stats.loss_deals += 1
        self.stats.total_commission += self.deal_commission
        self.stats.bank += profit

    # проверить, выполнено ли условие по старту сделки
    def run_start_deal(self):
        deal_type = ''
        is_in_deal = False
        if self.is_start_deal(is_buy=True):
            deal_type = 'buy'
            is_in_deal = True
        elif self.is_start_deal(is_buy=False):
            deal_type = 'sell'
            is_in_deal = True

        if is_in_deal:
            start_price = self.price.close
            # определим тейк-профит и стоп-лосс
            if deal_type == 'buy':
                take_profit_price = start_price + self.take_profit
                stop_loss_price = start_price - self.stop_loss
            else:
                take_profit_price = start_price - self.take_profit
                stop_loss_price = start_price + self.stop_loss
            self.print_start_deal(deal_type, start_price, self.price.date, take_profit_price, stop_loss_price)
            return {'start_price': start_price,
                    'take_profit_price': take_profit_price,
                    'stop_loss_price': stop_loss_price,
                    'deal_type': deal_type}

    def run(self):
        is_in_deal: bool = False
        start_price: float = 0.0
        take_profit_price: float = 0.0
        stop_loss_price: float = 0.0
        deal_type: str = ''  # buy/sell

        for c_index, c_date, c_open, c_close, c_high, c_low in zip(self.data['index'],
                                                                   self.data['date'],
                                                                   self.data['open'],
                                                                   self.data['close'],
                                                                   self.data['high'],
                                                                   self.data['low']
                                                                   ):
            self.price.index = c_index
            self.price.date = c_date
            self.price.open = c_open
            self.price.close = c_close
            self.price.high = c_high
            self.price.low = c_low

            # старт сделки
            if not is_in_deal:
                res_start_deal = self.run_start_deal()
                if res_start_deal is not None:
                    is_in_deal = True
                    start_price = res_start_deal['start_price']
                    take_profit_price = res_start_deal['take_profit_price']
                    stop_loss_price = res_start_deal['stop_loss_price']
                    deal_type = res_start_deal['deal_type']
            # завершение сделки - по стоп-лоссу/тейк-профиту или иному условию
            else:
                is_buy = True if deal_type == 'buy' else False
                stop_loss_check = self.is_stop_loss(is_buy=is_buy, stop_loss_price=stop_loss_price)
                take_profit_check = self.is_take_profit(is_buy=is_buy, take_profit_price=take_profit_price)
                end_deal_check = self.is_end_deal(is_buy=is_buy, start_price=start_price)
                
                # если на свече одновременно реализуется стоп-лосс и тейк-профит
                # необходимо на более мелком масштабе определить, что наступило раньше
                if stop_loss_check and take_profit_check:
                    high = take_profit_price if is_buy else stop_loss_price
                    low = stop_loss_price if is_buy else take_profit_price

                    add_minutes = 0
                    if self.main_time_frame == '1hour':
                        add_minutes = 60
                    date_from = self.price.date + timedelta(minutes=1)
                    date_to = date_from + timedelta(minutes=add_minutes-1)
                    print('----------------------------------------------------------------------------')
                    print("date_from=", date_from, "date_to=", date_to)
                    res_dates = self.db.who_1st_stop_loss_or_take_profit(ticker=self.ticker,
                                                                         date_from=date_from, date_to=date_to,
                                                                         high=high, low=low)
                    print('high=', high, 'low=', low)
                    date_low = None
                    date_high = None

                    for row in res_dates:
                        if row['target'] == 'low':
                            date_low = row['date']
                        if row['target'] == 'high':
                            date_high = row['date']

                    print("date_low = ", date_low, "date_high = ", date_high)
                    if None not in (date_low, date_to):

                        if is_buy:
                            # take-profit
                            if date_high < date_low:
                                profit = take_profit_price - start_price
                                result_end = 'take_profit'
                                print('buy ------take-profit -------------------')
                            # stop-loss
                            else:
                                profit = stop_loss_price - start_price
                                result_end = 'stop_loss'
                                print('buy ------stop-loss -------------------')

                        else:
                            if date_high > date_low:
                                print('sell ------take-profit -------------------')
                                # take-profit
                                pass
                            else:
                                # stop-loss
                                print('sell ------stop-loss -------------------')
                                pass
                        is_in_deal = False
                        self.add_stat(profit)
                        self.print_end_deal(deal_type, result_end, profit, self.price, self.price.date)

                    else:
                        raise Exception('no both dates from self.db.who_1st_stop_loss_or_take_profit()')
                    
                    
                    
                else:
                    profit = None
                    result_end = None
                    is_in_deal = False if stop_loss_check or take_profit_check or end_deal_check else True                    
                    # --> стоп-лосс
                    if stop_loss_check:
                        profit = (stop_loss_price - start_price) if is_buy else (start_price - stop_loss_price)
                        result_end = 'stop_loss'
                    # --> тейк-профит
                    elif take_profit_check:
                        profit = (take_profit_price - start_price) if is_buy else (start_price - take_profit_price)
                        result_end = 'take_profit'                    
                    # --> по условию (is_end_deal)
                    elif end_deal_check:
                        profit = (self.end_deal_price - start_price) if is_buy else (start_price - self.end_deal_price)
                        result_end = 'end_deal' 
                    if not is_in_deal:
                        self.add_stat(profit)
                        self.print_end_deal(deal_type, result_end, profit, self.price, self.price.date)               

                # если сделка завершилась, но можно сразу открыть новую
                if not is_in_deal and self.is_open_new_after_closing:
                    res_start_deal = self.run_start_deal()
                    if res_start_deal is not None:
                        is_in_deal = True
                        start_price = res_start_deal['start_price']
                        take_profit_price = res_start_deal['take_profit_price']
                        stop_loss_price = res_start_deal['stop_loss_price']
                        deal_type = res_start_deal['deal_type']



        self.stats.total_commission = round(self.stats.total_commission, 2)
        self.stats.bank_with_comm = self.stats.bank - self.stats.total_commission
