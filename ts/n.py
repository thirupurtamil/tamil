import requests 
import time
import pandas as pd
import numpy as np

from jugaad_data.nse import *


n = NSELive()     

ni = n.live_index('NIFTY 50')
r = ni['data'][0]['lastPrice']
f = int(ni['data'][0]['lastPrice']-ni['data'][0]['open'])
dt = ni['timestamp']

t = dt.split(" ")


data=[]


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',}
with requests.session() as req:
    req.get('https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY',headers = headers)

    api_req=req.get('https://www.nseindia.com/api/quote-derivative?symbol=NIFTY',headers = headers).json()
    for item in api_req['stocks']:
        data.append([
            
            item['metadata']['strikePrice'],
            item['metadata']['optionType'],
            
            item['metadata']['numberOfContractsTraded'],
            item['metadata']['totalTurnover'],]),



    

           


           



df = pd.DataFrame(data)
#rd = np.array(data)

#rs = rd.tolist([0])

#rs = df[df['strikePrice'] == df['strikePrice']]  



g = df.head(6)

#print(rs)
print (g)
print("|--------------------------------|")
print( "       ",t[1],r,[f])
print("|--------------------------------|")
      





      






