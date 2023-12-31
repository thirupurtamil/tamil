import requests
import pandas as pd
import time
import numpy as np

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
    
    iv = rdata ['records']['data']
    dt = rdata['records']['timestamp']


    data = { 
            "iv" : iv
             }
    return data


data = importdata()




print(data["iv"])


