from django.shortcuts import render
from sklearn import linear_model
import json
from binance.client import Client
import requests
import os
from django.shortcuts import render,HttpResponse
import sqlite3
from sklearn import linear_model
import pandas
import sqlalchemy
from binance.client import Client
import json
from binance.exceptions import BinanceAPIException


def pBit(request):
    
    symbol='BTCUSDT'    
    os.chdir('<database_directory>')
    engine=sqlalchemy.create_engine('sqlite:///crypto.db')
    btc=pandas.read_sql('coin_Bitcoin',engine)
    btc=pandas.DataFrame({'Symbol':'BTC','High':btc['High'],'Low':btc['Low'],'Open':btc['Open'],'Volume':btc['Volume'],'Marketcap':btc['Marketcap']})

    reg=linear_model.LinearRegression()
    reg.fit(btc[['Low', 'Open', 'Volume', 'Marketcap']],btc.High)
    
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    response = requests.get(url)
    data = response.json()
    print(data)
    t1 = data["market_data"]["low_24h"]["usd"]
    t2 = data["market_data"]["current_price"]["usd"]
    t3 = data["market_data"]["total_volume"]["usd"]
    t4 = data["market_data"]["market_cap"]["usd"]
    
    k=[t1,t2,t3,t4]
    data=float(reg.predict([k]))
    print(t2)
    quantity=float(request.POST.get('quantity'))
    if quantity<0.25:
        quantity=0.25
    
    with open('credentials.json', 'r') as f:
        c = json.load(f)
        if c['BTCacc']<0:
            data=0.8*data
        client = Client(c["api_key"],c["api_secret"],testnet = True)

        try:
            if data>t2:
                client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=quantity)
                client.futures_create_order(symbol=symbol,side='SELL',type='STOP_MARKET',stopPrice=round(0.9*t2,2),closePosition='true',quantity=quantity)
                client.futures_create_order(symbol=symbol,side='SELL',type='TAKE_PROFIT_MARKET',stopPrice=round(data,2),closePosition='true',quantity=quantity)
            else:
                return render(request,'alert_time.html')
        except BinanceAPIException:
            return render(request,'alert.html')

    return render(request,'home.html')

