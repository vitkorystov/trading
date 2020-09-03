from dataclasses import dataclass
from datetime import datetime


# дата класс для ТЕКУЩИХ параметров
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
    def __init__(self, data, start_index):
        self.data = data
        self.start_index = start_index
        self.stop_loss_price = None
        self.take_profit_price = None
        self.stats = Statistic()
        self.price = Price()
        # ----------------- параметры -------------------------
        self.is_print = True
        self.deal_commission = 0
        # если сделка завершилась, но нужно сразу открыть новую
        self.is_open_new_after_closing = True

    # условие старта сделки --> покупки/продажи
    # is_buy -> True=buy, False=sell
    def is_start_deal(self, is_buy):
        pass

    # условие по тейк-профиту - возвращает True/False
    def is_take_profit(self, is_buy, start_price):
        pass

    # условие по стоп-лоссу - возвращает True/False
    def is_stop_loss(self, is_buy, start_price):
        pass

    def print_end_deal(self, deal_type, deal_res, profit, price, date):
        if self.is_print:
            print(f'finish-->  deal_type: {deal_type}, closed by: {deal_res}, profit={profit} \n'
                  f'{price}, date: {date} \n')

    def print_start_deal(self, deal_type, start_price, date):
        if self.is_print:
            print(f'start-->  deal_type: {deal_type}, start_price: {start_price},  date: {date}')

    def add_stat(self, profit):
        if profit >= 0:
            self.stats.profit_deals += 1
        else:
            self.stats.loss_deals += 1
        self.stats.total_commission += self.deal_commission
        self.stats.bank += profit

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
            self.print_start_deal(deal_type, start_price, self.price.date)
            return {'start_price': start_price,
                    'deal_type': deal_type}

    def run(self):
        is_in_deal: bool = False
        start_price: float = 0.0
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
                    deal_type = res_start_deal['deal_type']
                    continue
            # завершение сделки - по стоп-лоссу или тейк-профиту
            else:
                # завершение сделки на покупку (buy)
                if deal_type == 'buy':
                    if self.is_stop_loss(is_buy=True, start_price=start_price):
                        profit = self.stop_loss_price - start_price
                        self.add_stat(profit)
                        is_in_deal = False
                        self.print_end_deal(deal_type, 'stop_loss', profit, self.price, self.price.date)

                    elif self.is_take_profit(is_buy=True, start_price=start_price):
                        profit = self.take_profit_price - start_price
                        self.add_stat(profit)
                        is_in_deal = False
                        self.print_end_deal(deal_type, 'take_profit', profit, self.price, self.price.date)

                # завершение сделки на продажу (sell)
                else:
                    if self.is_stop_loss(is_buy=False, start_price=start_price):
                        profit = start_price - self.stop_loss_price
                        self.add_stat(profit)
                        is_in_deal = False
                        self.print_end_deal(deal_type, 'stop_loss', profit, self.price, self.price.date)
                    elif self.is_take_profit(is_buy=False, start_price=start_price):
                        profit = start_price - self.take_profit_price
                        self.add_stat(profit)
                        is_in_deal = False
                        self.print_end_deal(deal_type, 'take_profit', profit, self.price, self.price.date)

                # если сделка завершилась, но можно сразу открыть новую
                if not is_in_deal and self.is_open_new_after_closing:
                    res_start_deal = self.run_start_deal()
                    if res_start_deal is not None:
                        is_in_deal = True
                        start_price = res_start_deal['start_price']
                        deal_type = res_start_deal['deal_type']
                        continue

        self.stats.total_commission = round(self.stats.total_commission, 2)
        self.stats.bank_with_comm = self.stats.bank - self.stats.total_commission
