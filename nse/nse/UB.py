import requests 
import time
import pandas as pd
import numpy as np

from jugaad_data.nse import *

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
ds = df.head(14)          

dx= ds.pivot_table(index = ['OPTION'], aggfunc ='size') 
print(dx)
print("---------------------")     

dss = df.filter(['STRIKEPRICE','OPTION',])
dss = dss.head(14)
de= dss.pivot_table(index = ['OPTION'], aggfunc ='max')
print("HIGH:",de)
print("---------------------")     
de1= dss.pivot_table(index = ['OPTION'], aggfunc ='min')
print("LOW:",de1)
print("---------------------")     

























