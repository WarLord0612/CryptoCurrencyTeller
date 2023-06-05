from django.shortcuts import render
import json
import os
from django.shortcuts import render,HttpResponse
from sklearn import linear_model
import pandas
import sqlalchemy
import requests
from binance.client import Client
from binance.exceptions import BinanceAPIException

def pXrp(request):
    symbol='XRPUSDT'
    os.chdir('<database_directory>')
    engine = sqlalchemy.create_engine('sqlite:///crypto.db')
    xrp=pandas.read_sql('coin_XRP',engine)
    xrp=pandas.DataFrame({'Symbol':'XRP','High':xrp['High'],'Low':xrp['Low'],'Open':xrp['Open'],'Volume':xrp['Volume'],'Marketcap':xrp['Marketcap']})
    xrp.to_sql('coin_XRP',engine,if_exists='replace',index=False)
    
    reg3 = linear_model.LinearRegression()
    reg3= reg3.fit(xrp[['Low', 'Open', 'Volume', 'Marketcap']],xrp.High)

    url = "https://api.coingecko.com/api/v3/coins/ripple"

    response = requests.get(url)

    data = response.json()
    t1 = data["market_data"]["low_24h"]["usd"]
    t2 = data["market_data"]["current_price"]["usd"]
    t3 = data["market_data"]["total_volume"]["usd"]
    t4 = data["market_data"]["market_cap"]["usd"]
    
    k=[t1,t2,t3,t4]
    data=float(reg3.predict([k]))
    
    quantity=float(request.POST.get('quantity'))
    if quantity<5000:
        quantity=5000

    with open('credentials.json', 'r') as f:
        c = json.load(f)
        if c['XRPacc']<0:
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

