from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sklearn import linear_model
from time import sleep
import os
from django.shortcuts import render,HttpResponse
import sqlite3
from sklearn import linear_model
from selenium import webdriver
import pandas
import sqlalchemy
import json
from binance.exceptions import BinanceAPIException

def pDoge(request):
    
    symbol='DOGEUSDT'
    import requests
    from binance.client import Client
    os.chdir('<database_directory>')
    engine = sqlalchemy.create_engine('sqlite:///crypto.db')
    doge=pandas.read_sql('coin_Dogecoin',engine)
    doge=pandas.DataFrame({'Symbol':'DOGE','High':doge['High'],'Low':doge['Low'],'Open':doge['Open'],'Volume':doge['Volume'],'Marketcap':doge['Marketcap']})
    doge.to_sql('coin_Dogecoin',engine,if_exists='replace',index=False)
    
    reg5 = linear_model.LinearRegression()
    reg5= reg5.fit(doge[['Low', 'Open', 'Volume', 'Marketcap']],doge.High)

    url = "https://api.coingecko.com/api/v3/coins/dogecoin"

    response = requests.get(url)

    data = response.json()
    t1 = data["market_data"]["low_24h"]["usd"]
    t2 = data["market_data"]["current_price"]["usd"]
    t3 = data["market_data"]["total_volume"]["usd"]
    t4 = data["market_data"]["market_cap"]["usd"]
    
    k=[t1,t2,t3,t4]
    data=float(reg5.predict([k]))
    quantity=float(request.POST.get('quantity'))
    if quantity<1000:
        quantity=1000
    
    with open('credentials.json', 'r') as f:
        c = json.load(f)
        if c['DOGEacc']<0:
            data=0.8*data
        client = Client(c["api_key"],c["api_secret"],testnet = True)

        try:
            if data>t2:
                c=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=quantity)
                c=client.futures_create_order(symbol=symbol,side='SELL',type='STOP_MARKET',stopPrice=round(0.9*t2,3),closePosition='true',quantity=quantity)
                c=client.futures_create_order(symbol=symbol,side='SELL',type='TAKE_PROFIT_MARKET',stopPrice=round(data,3),closePosition='true',quantity=quantity)
            else:
                return render(request,'alert_time.html')
        except BinanceAPIException:
            return render(request,'alert.html')
        


    
    return render(request,'home.html')

