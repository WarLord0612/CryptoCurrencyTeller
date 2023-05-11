from django.shortcuts import render,HttpResponse
import sqlalchemy
import pandas
from sklearn import linear_model
import os
from time import sleep
import requests



from matplotlib import pyplot
# Create your views here.
def Bitcoin(request):
    os.chdir(r'C:\Users\mohan\Desktop')
    engine=sqlalchemy.create_engine('sqlite:///crypto.db')
    btc=pandas.read_sql('coin_Bitcoin',engine)
    btc=pandas.DataFrame({'Symbol':'BTC','High':btc['High'],'Low':btc['Low'],'Open':btc['Open'],'Volume':btc['Volume'],'Marketcap':btc['Marketcap']})
    btc.to_sql('coin_Bitcoin',engine,if_exists='replace',index=False)
    reg=linear_model.LinearRegression()
    reg.fit(btc[['Low', 'Open', 'Volume', 'Marketcap']],btc.High)
    


    url = "https://api.coingecko.com/api/v3/coins/bitcoin"

    response = requests.get(url)

    data = response.json()
    t1 = data["market_data"]["low_24h"]["usd"]
    t2 = data["market_data"]["current_price"]["usd"]
    t3 = data["market_data"]["total_volume"]["usd"]
    t4 = data["market_data"]["market_cap"]["usd"]



    k=[t1,t2,t3,t4]
    data=float(reg.predict([k]))
    import json
    with open(r'C:\Users\mohan\Desktop\CryptoCurrencyTeller\credentials.json','r') as f:
        c=json.load(f)

    pyplot.plot(range(1,11),list(btc.tail(10)['High'].to_numpy()),label="Bitcoin's performance",marker='o',markerfacecolor='blue')
    pyplot.title("Bitcoin's performance over last 10 days:")
    pyplot.ylabel('Price ($)')
    pyplot.xlabel('Days')
    pyplot.grid(True,linewidth=1,linestyle='-.')
    pyplot.legend(loc='upper right')
    pyplot.savefig(r'C:\Users\mohan\Desktop\CryptoCurrencyTeller\CryptoCurrencyTeller\static\plot1.png',dpi=500)
      
    pyplot.close()
    if c['BTCacc']<0:
        data=0.95*data
    return render(request,'home1.html',{'data':data})

