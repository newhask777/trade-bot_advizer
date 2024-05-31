from tradingview_ta import TA_Handler, Interval, Exchange
from binance.um_futures import UMFutures
from binance.cm_futures  import CMFutures
import json
import time
import requests


INTERVAL = Interval.INTERVAL_15_MINUTES
TELEGRAM_TOKEN = '7303689534:AAGIP0NqABu1h6XqV4k029qBvBVCGzguq_E'
TELEGRAM_CHANNEL = '5650732610'


client = UMFutures()

# print(client)

def get_data(symbol):
    output = TA_Handler(
        symbol=symbol,
        screener="Crypto",
        exchange="Binance",
        interval=INTERVAL
    )
    
     
    activiti = output.get_analysis().summary
    # print(activiti)
    activiti['SYMBOL'] = symbol
    return activiti


def get_symbols():
    tickers = client.mark_price()
    symbols = []

    for i in tickers:
        ticker = i['symbol']
        symbols.append(ticker)

    print(symbols)
    
    return symbols

# get_symbols()


def send_message(text):
    res = requests.get(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', params=dict(
        chat_id=TELEGRAM_CHANNEL, text=text
    ))

# send_message('dfgdg')


symbols = get_symbols()
longs = []
shorts = []


def first_data():
    print('Search first data')
    send_message('Search first data')
    for i in symbols:
        try:
            data = get_data(i)

            # print(data)

            if(data['RECOMMENDATION'] == 'STRONG_BUY'):
                longs.append(data['SYMBOL'])
                
            if(data['RECOMMENDATION'] == 'STRONG_SELL'):
                shorts.append(data['SYMBOL'])

            time.sleep(0.01)
            
        except:
            pass

    print('longs: ')
    print(longs)
    print('shorts: ')
    print(shorts)
    return longs, shorts

print('Start')
send_message('Start')
first_data()

while True:
    print('______________________NEW ROUND___________________________')

    for i in symbols:
        try:
            data = get_data(i)

            if(data['RECOMMENDATION'] == 'STRONG_BUY' and (data['SYMBOL'] not in longs)):
                print(data['SYMBOL'], 'Buy')
                text = data['SYMBOL'] + ' BUY'
                send_message(text)
                longs.append(data['SYMBOL'])

            if(data['RECOMMENDATION'] == 'STRONG_SELL' and (data['SYMBOL'] not in shorts)):
                print(data['SYMBOL'], 'Sell')
                text = data['SYMBOL'] + ' SELL'
                send_message(text)
                longs.append(data['SYMBOL'])
            time.sleep(0.1)

        except:
            pass







    