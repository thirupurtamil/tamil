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

data = importdata()




print("|{:<9}|OI :{:<12}| OI:{:<12}| {:<10}|".format(data["Time"],data["COI"],data["POI"],data["Trend"]))

print("|-------------------------------------------------------|")




print("|{:<9}|VOL:{:<12}|VOL:{:<12}|{:<11}|".format(data["Time"],data["tc"],data["tp"],data["Tr"]))

print("|-------------------------------------------------------|")











    



 














