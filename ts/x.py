import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

url = "https://chartink.com/screener/process"

condition = {"scan_clause" : "( {cash} ( latest rsi( 9 ) > latest wma( latest rsi( 9 ) , 21 ) and 1 day ago  rsi( 9 ) <= 1 day ago  wma( latest rsi( 9 ) , 21 ) and latest rsi( 9 ) > 70 and market cap > 1500 ) ) "}

with requests.session() as s:
    r_data = s.get(url)
    soup = bs(r_data.content, "lxml")
    meta = soup.find("meta", {"name" : "csrf-token"})["content"]

    header = {"x-csrf-token" : meta}
    data = s.post(url, headers=header, data=condition).json()

    stock_list = pd.DataFrame(data["data"])
    print(stock_list)
