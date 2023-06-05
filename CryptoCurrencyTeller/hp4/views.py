from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import requests
import os
import pandas
import sqlalchemy
from sklearn import linear_model

# Create your views here.
def Avalanche(request):
    os.chdir('<database_directory>')
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
    import json
    with open('credentials.json','r') as f:
        c=json.load(f)
      
    from matplotlib import pyplot
    pyplot.plot(range(1,11),list(aave.tail(10)['High'].to_numpy()),label="Aave's performance",marker='o',markerfacecolor='blue')
    pyplot.title("Aave's performance over last 10 days:")
    pyplot.ylabel('Price ($)')
    pyplot.xlabel('Days')
    pyplot.grid(True,linewidth=1,linestyle='-.')
    pyplot.legend(loc='upper right')
    pyplot.savefig('CryptoCurrencyTeller\static\plot4.png',dpi=500)
    pyplot.close()
    if c['AAVEacc']<0:
        data=0.95*data
    return render(request,'home4.html',{'data':data})