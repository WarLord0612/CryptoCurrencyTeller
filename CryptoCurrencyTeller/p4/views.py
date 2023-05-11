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
import requests
from binance.client import Client
import json
from binance.exceptions import BinanceAPIException

def pAave(request):

    symbol='AAVEUSDT'
    os.chdir(r'C:\Users\mohan\Desktop')
    engine = sqlalchemy.create_engine('sqlite:///crypto.db')
    aave=pandas.read_sql('coin_Aave',engine)
    aave=pandas.DataFrame({'Symbol':'AAVE','High':aave['High'],'Low':aave['Low'],'Open':aave['Open'],'Volume':aave['Volume'],'Marketcap':aave['Marketcap']})
    aave.to_sql('coin_Aave',engine,if_exists='replace',index=False)
    
    reg4 = linear_model.LinearRegression()
    reg4= reg4.fit(aave[['Low', 'Open', 'Volume', 'Marketcap']],aave.High)

    url = "https://api.coingecko.com/api/v3/coins/aave"

    response = requests.get(url)

    data = response.json()
    t1 = data["market_data"]["low_24h"]["usd"]
    t2 = data["market_data"]["current_price"]["usd"]
    t3 = data["market_data"]["total_volume"]["usd"]
    t4 = data["market_data"]["market_cap"]["usd"]
    
    k=[t1,t2,t3,t4]
    data=float(reg4.predict([k]))
    
    quantity=float(request.POST.get('quantity'))
    
    with open(r'C:\Users\mohan\Desktop\CryptoCurrencyTeller\credentials.json', 'r') as f:
        c = json.load(f)
        if c['AAVEacc']<0:
            data=0.95*data

        client = Client(c["api_key"],c["api_secret"],testnet = True)

        try:
            if data>t2:
                client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=quantity)
                client.futures_create_order(symbol=symbol,side='SELL',type='STOP_MARKET',stopPrice=round(0.9*t2,3),closePosition='true',quantity=quantity)
            
                client.futures_create_order(symbol=symbol,side='SELL',type='TAKE_PROFIT_MARKET',stopPrice=round(data,3),closePosition='true',quantity=quantity)

        except BinanceAPIException:
            return render(request,'alert.html')

    
    return render(request,'home.html')
