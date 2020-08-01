import pandas as pd

file = 'futures/SPFB.Si-9.20_200401_200801.csv'
df = pd.read_csv(file, sep=';')




is_deal = False
start_deal = 0
deal_type = ''
deal_duration = 0
take_profit = 0
stop_loss = 0

deal_end_type = ''

spreads = [abs(row['<HIGH>']-row['<LOW>']) for i, row in df.iterrows()]
print(max(spreads), min(spreads))

for r in spreads:
    if r > 100:
        print(r)






'''
for i, row in df.iterrows():
    open = row['<OPEN>']
    close = row['<CLOSE>']
    high = row['<HIGH>']
    low = row['<LOW>']

    # print(i, open, close, high, low)


    
    if not is_deal:
        start_deal = open

        # начальная сделка
        if i == 0:
            deal_type = 'buy'

        if deal_type == 'buy':
            take_profit = start_deal + 10
            stop_loss = start_deal - 10
        else:
            take_profit = start_deal - 10
            stop_loss = start_deal + 10

        print(f"Сделка открыта: i={i}, тип: {deal_type}, start_deal={start_deal}, take_profit={take_profit}, stop_loss={stop_loss}")
        is_deal = True

    # ловим окончание сделки
    if is_deal:
        deal_duration += 1
        # закрытие сделки при покупке
        if deal_type == 'buy':
            if high > take_profit:
                deal_end_type = 'profit'
                is_deal = False
                break
            if low < stop_loss:
                deal_end_type = 'loss'
                is_deal = False
                break
        # закрытие сделки при продажe
        if deal_type == 'sell':
            if low < take_profit:
                deal_end_type = 'profit'
                is_deal = False
                break
            if high > stop_loss:
                deal_end_type = 'loss'
                is_deal = False
                break
'''

















