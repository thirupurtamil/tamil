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
    
    
    rd = format(rs-ni, ".2f")
    t = dt.split(" ")

    date_dict = {'index_date':date ,'empname':name , 'greetings':msg, 'count':count , 'n' :nf, 'rs' :rs, 'rd' :rd,'h' : rm,  "d" : t[1],}
    return render (request,'papa/pa.html',context =date_dict)













    
    













