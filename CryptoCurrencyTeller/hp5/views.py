from django.shortcuts import render
import requests
import os
import pandas
import sqlalchemy
from sklearn import linear_model

# Create your views here.
def Dogecoin(request):
    os.chdir(r'C:\Users\mohan\Desktop')
    engine = sqlalchemy.create_engine('sqlite:///crypto.db')
    doge=pandas.read_sql('coin_Dogecoin',engine)
    doge=pandas.DataFrame({'Symbol':'DOGE','High':doge['High'],'Low':doge['Low'],'Open':doge['Open'],'Volume':doge['Volume'],'Marketcap':doge['Marketcap']})
    doge.to_sql('coin_Dogecoin',engine,if_exists='replace',index=False)
    
    reg5=linear_model.LinearRegression()
    reg5.fit(doge[['Low', 'Open', 'Volume', 'Marketcap']],doge.High)

    url = "https://api.coingecko.com/api/v3/coins/dogecoin"

    response = requests.get(url)

    data = response.json()
    t1 = data["market_data"]["low_24h"]["usd"]
    t2 = data["market_data"]["current_price"]["usd"]
    t3 = data["market_data"]["total_volume"]["usd"]
    t4 = data["market_data"]["market_cap"]["usd"]
    k=[t1,t2,t3,t4]
    data=float(reg5.predict([k]))
    import json
    with open(r'C:\Users\mohan\Desktop\CryptoCurrencyTeller\credentials.json','r') as f:
        c=json.load(f)
      
    from matplotlib import pyplot
    pyplot.plot(range(1,11),list(doge.tail(10)['High'].to_numpy()),label="Dogecoin's performance",marker='o',markerfacecolor='blue')
    pyplot.title("Dogecoin's performance over last 10 days:")
    pyplot.ylabel('Price ($)')
    pyplot.xlabel('Days')
    pyplot.grid(True,linewidth=1,linestyle='-.')
    pyplot.legend(loc='upper right')
    pyplot.savefig(r'C:\Users\mohan\Desktop\CryptoCurrencyTeller\CryptoCurrencyTeller\static\plot5.png',dpi=500)
    
    pyplot.close()
    if c['BTCacc']<0:
        data=0.95*data
    return render(request,'home5.html',{'data':data})
   