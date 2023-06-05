from django.shortcuts import render
import requests
import os
import pandas
import sqlalchemy
from sklearn import linear_model
from time import sleep



# Create your views here.
def Ethereum(request):
    os.chdir('<database_directory>')
    engine = sqlalchemy.create_engine('sqlite:///crypto.db')
    eth=pandas.read_sql('coin_Ethereum',engine)
    eth=pandas.DataFrame({'Symbol':'ETH','High':eth['High'],'Low':eth['Low'],'Open':eth['Open'],'Volume':eth['Volume'],'Marketcap':eth['Marketcap']})
    eth.to_sql('coin_Ethereum',engine,if_exists='replace',index=False)
    
    reg2 = linear_model.LinearRegression()
    reg2= reg2.fit(eth[['Low', 'Open', 'Volume', 'Marketcap']],eth.High)
    
    url = "https://api.coingecko.com/api/v3/coins/ethereum"

    response = requests.get(url)

    data = response.json()
    t1 = data["market_data"]["low_24h"]["usd"]
    t2 = data["market_data"]["current_price"]["usd"]
    t3 = data["market_data"]["total_volume"]["usd"]
    t4 = data["market_data"]["market_cap"]["usd"]
   
    
  
    k=[t1,t2,t3,t4]
    data=float(reg2.predict([k]))
    import json
    with open('credentials.json','r') as f:
        c=json.load(f)

    from matplotlib import pyplot
    pyplot.plot(range(1,11),list(eth.tail(10)['High'].to_numpy()),label="Ethereum's performance",marker='o',markerfacecolor='blue')
    pyplot.title("Ethereum's performance over last 10 days:")
    pyplot.ylabel('Price ($)')
    pyplot.xlabel('Days')
    pyplot.grid(True,linewidth=1,linestyle='-.')
    pyplot.legend(loc='upper right')
    pyplot.savefig('CryptoCurrencyTeller\static\plot2.png',dpi=500)
    pyplot.close()
    if c['ETHacc']<0:
        data=0.95*data
    return render(request,'home2.html',{'data':data})