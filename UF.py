import requests
import pandas as pd
import time
import numpy as np

url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37','accept-encoding': 'gzip, deflate, br','accept-language': 'en-GB,en;q=0.9,en-US;q=0.8'}

session = requests.Session()
request = session.get(url,headers=headers)
cookies = dict(request.cookies)


def dataframe():
    response = session.get(url,headers=headers,cookies=cookies).json()
    rawdata = pd.DataFrame(response) 
    rawop = pd.DataFrame(rawdata['filtered']['data']).fillna(0)
    data = []
    for i in range(0,len(rawop)):
        calloi = callcoi = cltp = putoi = putcoi = pltp = 0
        stp = rawop['strikePrice'][i]
     
     
        if(rawop['CE'][i]==0):
            calloi = callcoi = 0
        else:
            calloi = rawop['CE'][i]['openInterest']
            callcoi = rawop['CE'][i]['changeinOpenInterest']
            cltp = rawop['CE'][i]['lastPrice']
            civ = rawop['CE'][i]['impliedVolatility']

        if(rawop['PE'][i] == 0):
            putoi = putcoi = 0
        else:
            putoi = rawop['PE'][i]['openInterest']
            putcoi = rawop['PE'][i]['changeinOpenInterest']
            pltp = rawop['PE'][i]['lastPrice']
            piv = rawop['PE'][i]['impliedVolatility']
            live = rawop['PE'][i]['underlyingValue']
    
        opdata = {
            'CALL OI': calloi, 'CALL CHNG OI': callcoi, 'CALL LTP': cltp,  'C-IV': civ,'STRIKE PRICE': stp,
           
            'PUT OI': putoi, 'PUT CHNG OI': putcoi, 'PUT LTP': pltp,'P-IV': piv,'LIV' : live,
        }
        
        data.append(opdata)
    optionchain = pd.DataFrame(data)
    return optionchain

optionchain = dataframe()
op = optionchain.head(90)


opd = optionchain.set_index("STRIKE PRICE")
oph = opd.iloc[-47:-9] 
opc = oph.filter((["CALL OI"])).idxmax()
opp = oph.filter((["PUT OI"])).idxmax()



rs = dataframe()

rs = rs.head(60)

oph=oph.filter(['STRIKE PRICE','C-IV','P-IV'])
oph=oph.head(20)
print("-------------------------")
print(oph)









