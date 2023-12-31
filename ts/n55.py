from nsepython import * 
from jugaad_data.nse import *
from pprint import pprint
import webbrowser
from time import sleep
from nsetools import *
from nsepython import * 
from jugaad_data.nse import *
from pprint import pprint
import webbrowser
from time import sleep
import requests
import pandas as pd
import time
import json
from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
import pandas as pd
import time
from datetime import *
from time import *






url = 'https://www.nseindia.com/api/chart-databyindex?index=NIFTY%2050&indices=true&preopen=true'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
            
           'accept-language': 'en,gu;q=0.9,hi;q=0.8',
           'accept-encoding': 'gzip, deflate, br'}

session = requests.Session()

def importdata():
    request = session.get(url,headers=headers)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, cookies=cookies).json()['grapthData']
    rdata = pd.DataFrame(response)
    

    ce = rdata.head(600)
    t_ce = ce.iloc[: , 1:]

    data = { "COI" : t_ce,
             }
    return data
    
    
   
while True:
    data = importdata()
    
    print("PRE OPEN")
    print("|------------------HIGH------------------------------|")


    print ((data["COI"]).max())
    print("|------------------LOW-------------------------------|")


    print ((data["COI"]).min())
    print("|------------------HIGH------------------------------|")
    break 

    
    
   
  

    
    
   
  
nse_obj = Nse()  
n = NSELive()     
nse = Nse()
nifty_data = n.live_index('NIFTY 50')


now = datetime.now() 
current_time = now.strftime("%H:%M:%S") 

def p_time(time): 
    return time.strftime('%I:%M %p') 
time = datetime.now() 
time_format = p_time(time) 



#print("NSE Object:", nse_obj)
#print(indices)
print("Name:",nifty_data['name'],)
print("Time:", nifty_data['timestamp'],) 
print("Last price:",nifty_data['data'][0]['lastPrice'],)
print("Open price:",nifty_data['data'][0]['open'],)
print("Daylow.   :",nifty_data['data'][0]['dayLow'],)
print("Dayhigh.  :",nifty_data['data'][0]['dayHigh'],)
print("Time:",time_format)















print("|------------------NIFTY-----------------------------|")




data=[]


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',}
with requests.session() as req:
    req.get('https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY',headers = headers)

    api_req=req.get('https://www.nseindia.com/api/quote-derivative?symbol=NIFTY',headers = headers).json()
    for item in api_req['stocks']:
        data.append([
            
            item['metadata']['strikePrice'],
            item['metadata']['optionType'],
            item['metadata']['openPrice'],
            item['metadata']["highPrice"],
            item['metadata']['lowPrice'],
            item['metadata']['lastPrice'],
            item['metadata']['numberOfContractsTraded'],
            item['metadata']['totalTurnover'],]),
            
           

cols=['STRIKEPRICE','OPTION','OPEN',"HIGH",'LOW','LAST','VOL','VALUE']
            
           



df = pd.DataFrame(data, columns=cols)

rs = df[df['OPEN'] == df['HIGH']]  
 


rs = rs.head(6)



get_rows = df.head(14)


print (get_rows)
print("|------------------NIFTY-----------------------------|")
print(rs)





import requests
import pandas as pd
import time

url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8',
           'accept-encoding': 'gzip, deflate, br'}

session = requests.Session()

def importdata():
    request = session.get(url,headers=headers)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, cookies=cookies).json()   
    rdata = pd.DataFrame(response)
    t_ce = rdata['filtered']['CE']['totOI']
    t_pe = rdata['filtered']['PE']['totOI']
    tc = rdata['filtered']['CE']['totVol']
    tp   = rdata['filtered']['PE']['totVol']
    dt = rdata['records']['timestamp']
    trend = t_pe - t_ce
    tr = tp - tc
    t = dt.split(" ")
    data = {
      "Time" : t[1],
      "COI" : t_ce,
      "POI" : t_pe,
      "tc" : tc,
      "tp" : tp,
      "Tr" : tr,
      "Trend" : trend
   }
    return data




    
print("|-------------------------------------------------------|")
print("|{:<9}| {:<15}| {:<15}| {:<10}|".format(" Time"," Total Call OI"," Total Put OI","Trend"))

print("|-------------------------------------------------------|")
while True:
   data = importdata()




   print("|{:<9}|CI :{:<12}| PI:{:<12}| {:<10}|".format(data["Time"],data["COI"],data["POI"],data["Trend"]))

   print("|-------------------------------------------------------|")




   print("|{:<9}|CEV:{:<12}|PEV:{:<12}|{:<11}|".format(data["Time"],data["tc"],data["tp"],data["Tr"]))

   print("|-------------------------------------------------------|")
   time.sleep(30)










    



 














