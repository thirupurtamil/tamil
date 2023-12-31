from jugaad_data.nse import NSELive
from django.shortcuts import render 
from django.http import HttpResponse
import datetime 
import platform 
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import requests 
import time
import pandas as pd
import numpy as np



def home(request):
    return render (request,'papa/home.html',{})


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
    t_ce = ce.iloc[: ,1:]
    ph = t_ce.max().to_string()
    pl = t_ce.min().to_string()
    
    data = { 'HIGH': ph ,'LOW': pl
     

           }
    return data



















def tss(request):
    msg = 'HAI'
    name = 'TAMIL'
    User = get_user_model()
    count= User.objects.count
    date = datetime.datetime.now()
    hour = int(date.strftime('%H'))
    if hour<12:
     msg+=  ',GOOD MORNING'
    else:
     msg+=  ',GOOD EVENING'
    
    
    n = NSELive()
    
    ns = n.live_index('NIFTY 50')
    nf = ns['data'][0]['open']
    ni = ns['data'][0]['previousClose']
    rs = ns['data'][0]['lastPrice']
    rm = ns['data'][0]['dayHigh']
    dt = ns['timestamp']
    ds = importdata()
    
    rd = format(rs-ni, ".2f")
    t = dt.split(" ")

    date_dict = {'index_date':date ,'empname':name , 'greetings':msg, 'count':count , 'n' :nf, 'rs' :rs, 'rd' :rd,'h' : rm,  "d" : t[1], 'c' : ds ,}
    return render (request,'papa/pa.html',context =date_dict)


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
        if(rawop['PE'][i] == 0):
            putoi = putcoi = 0
        else:
            putoi = rawop['PE'][i]['openInterest']
            putcoi = rawop['PE'][i]['changeinOpenInterest']
            pltp = rawop['PE'][i]['lastPrice']
        opdata = {
            'CALL OI': calloi, 'CALL CHNG OI': callcoi, 'CALL LTP': cltp, 'STRIKE PRICE': stp,
            'PUT OI': putoi, 'PUT CHNG OI': putcoi, 'PUT LTP': pltp,'r': data,
        }
        
        data.append(opdata)
    optionchain = pd.DataFrame(data)
    return optionchain



def raj(request):
    optionchain = dataframe()
    return render (request,'papa/pp.html',context = optionchain) 
















    
    













