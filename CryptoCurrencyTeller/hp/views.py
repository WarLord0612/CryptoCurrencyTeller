from django.shortcuts import render
from django.contrib import messages
from datetime import date
from datetime import datetime
from cryptocmd import CmcScraper
import pandas
import sqlalchemy
import os
from selenium import webdriver
import json
from time import sleep

# Create your views here.
def home(request):

    symbols=['AAVE','BTC','DOGE','ETH','XRP']
    tables=['coin_Aave','coin_Bitcoin','coin_Dogecoin','coin_Ethereum','coin_XRP']
    today = date.today()
    fh=open(r'C:\Users\mohan\Desktop\CryptoCurrencyTeller\date.txt','r')
    d2=str(fh.read())
    d2 =  datetime.strptime(d2, '%Y-%m-%d')
    fh.close()
    d1 =  date.today()
    fhw=open(r'C:\Users\mohan\Desktop\CryptoCurrencyTeller\date.txt','w')
    fhw.write(str(d1))
    fhw.close()
    d1 = datetime.strptime(str(d1), '%Y-%m-%d')
    

    delta = d1 - d2
    os.chdir('C:\\Users\\mohan\\Desktop')
    engine = sqlalchemy.create_engine("sqlite:///crypto.db")

    if delta.days!=0:
        for i in range(0,5):
            scraper = CmcScraper(symbols[i])
            df=scraper.get_dataframe().head(delta.days-1)
            df=df.iloc[::-1]
            d={'Symbol':symbols[i],'High':df['High'],'Low':df['Low'],'Open':df['Open'],'Volume':df['Volume'],'Marketcap':df['Market Cap']}
            df=pandas.DataFrame(d)
            df.to_sql(tables[i],engine,if_exists='append',index=False)

    with open(r'C:\Users\mohan\Desktop\CryptoCurrencyTeller\credentials.json','r') as f:
        c=dict(json.load(f))
        options=webdriver.ChromeOptions()
        #options.headless=True
        driver=webdriver.Chrome(options=options)
        driver.get("https://lunarcrush.com/coins/btc/bitcoin/galaxy-score")
        driver.maximize_window()
        sleep(6)
        t1=float(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[1]/div[2]/div[1]').text)                   
        t2=float(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[2]/div[3]/div[1]').text)
        c['BTCacc']=t1-t2                      

        driver.get("https://lunarcrush.com/coins/eth/ethereum/galaxy-score")
        driver.maximize_window()
        sleep(5)
        t1=float(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[1]/div[2]/div[1]').text)
        t2=float(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[2]/div[3]/div[1]').text)
        c['ETHacc']=t1-t2

        driver.get("https://lunarcrush.com/coins/xrp/ripple/galaxy-score")
        driver.maximize_window()
        sleep(5)
        t1=float(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[1]/div[2]/div[1]').text)
        t2=float(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[2]/div[3]/div[1]').text)
        c['XRPacc']=t1-t2

        driver.get("https://lunarcrush.com/coins/aave/aave/galaxy-score")
        driver.maximize_window()
        sleep(5)
        t1=float(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[1]/div[2]/div[1]').text)
        t2=float(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[2]/div[3]/div[1]').text)
        c['AAVEacc']=t1-t2

        driver.get("https://lunarcrush.com/coins/doge/dogecoin/galaxy-score")
        driver.maximize_window()
        sleep(5)
        t1=float(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[1]/div[2]/div[1]').text)
        t2=float(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[2]/div[3]/div[1]').text)
        c['DOGEacc']=t1-t2

        
        driver.quit()
        

    with open(r'C:\Users\mohan\Desktop\CryptoCurrencyTeller\credentials.json','w') as f1:
         json.dump(c,f1)
    
    return render(request,'signin.html')


    
def signin_evaluate(request):
    u=request.POST.get('email')
    p=request.POST.get('text')
    import json
    with open(r'C:\Users\mohan\Desktop\CryptoCurrencyTeller\credentials.json', 'r') as f:
                c = json.load(f)

    try :
        if c[u]==p:
            data='Signin Successful'
            return render(request,'home.html',{'data':data}) 
        else:  
            data="Invalid Password"
            return render(request,'signin.html',{'data':data})
    except NameError:
        data="Invalid Password"
        return render(request,'signin.html',{'data':data})
