from django.shortcuts import render
import requests
import os
import pandas
import sqlalchemy
from sklearn import linear_model


# Create your views here.
def Ripple(request):
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
    import json
    with open('credentials.json','r') as f:
        c=json.load(f)

    from matplotlib import pyplot
    pyplot.plot(range(1,11),list(xrp.tail(10)['High'].to_numpy()),label="Ripple's performance",marker='o',markerfacecolor='blue')
    pyplot.title("Ripple's performance over last 10 days:")
    pyplot.ylabel('Price ($)')
    pyplot.xlabel('Days')
    pyplot.grid(True,linewidth=1,linestyle='-.')
    pyplot.legend(loc='upper right')
    pyplot.savefig('CryptoCurrencyTeller\static\plot3.png',dpi=500)
    pyplot.close()
    if c['XRPacc']<0:
        data=0.95*data
    return render(request,'home3.html',{'data':data})
  