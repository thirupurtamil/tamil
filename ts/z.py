


from tkinter import *
from tkinter import ttk
import sqlite3
import threading
from kiteconnect import KiteConnect
root=Tk()
root.geometry("670x200")
root.config(background="black")
style= ttk.Style()
style.theme_use('winnative')
topFrame=Frame(root)
Button(topFrame,text="CONNECT",command=popup,width=20,bg="green4",fg="white",font=("Arial Black",10)).grid(row=0,column=0)
username=Label(topFrame,width=20,font=("Arial Black",10))
username.grid(row=0,column=1)
Button(topFrame,text="SL&QUANTITY",command=generateFields,width=20,bg="green4",fg="white",font=("Arial Black",10)).grid(row=0,column=2)

orderFrame=Frame(root)
Label(orderFrame,text="NAME",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=0,column=0)
name=Entry(orderFrame,font=("Arial Black",10))
name.grid(row=0,column=1)
Label(orderFrame,text="MARGIN",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=0,column=2)
margin=Entry(orderFrame,font=("Arial Black",10))
margin.grid(row=0,column=3)
Label(orderFrame,text="CAPITAL",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=1,column=0)
capital=Entry(orderFrame,font=("Arial Black",10))
capital.grid(row=1,column=1)
Label(orderFrame,text="LOSS",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=1,column=2)
loss=Entry(orderFrame,font=("Arial Black",10))
loss.grid(row=1,column=3)
Label(orderFrame,text="QUANTITY",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=2,column=0)
quantity=Entry(orderFrame,font=("Arial Black",10))
quantity.grid(row=2,column=1)
Label(orderFrame,text="STOP LOSS",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=2,column=2)
stoploss=Entry(orderFrame,font=("Arial Black",10))
stoploss.grid(row=2,column=3)
radio = IntVar()  
R1 = Radiobutton(orderFrame,width=15, text="MARKET",bg="gray10",fg="white",font=("Arial Black",10),selectcolor='green', variable=radio,value=1)
R1.grid(row = 3, column = 0)
R2 = Radiobutton(orderFrame,width=15, text="LIMIT",bg="gray10",fg="white",font=("Arial Black",10), selectcolor='green',variable=radio,value=2)
R2.grid(row = 3, column = 1)
Label(orderFrame,text="LAST PRICE",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=3,column=2)
ltp=Entry(orderFrame,font=("Arial Black",10))
ltp.grid(row=3,column=3)
radio2 = IntVar()  
R3 = Radiobutton(orderFrame,width=15, text="BUY",bg="gray10",fg="white",font=("Arial Black",10), selectcolor='green', variable=radio2,value=1)
R3.grid(row = 4, column = 0)
R4 = Radiobutton(orderFrame,width=15, text="SELL",bg="gray10",fg="white",font=("Arial Black",10), selectcolor='green', variable=radio2,value=2)
R4.grid(row = 4, column = 1)
Button(orderFrame,text="PLACE ORDER",width=18,bg="green4",fg="white",font=("Arial Black",10),command=placeOrder).grid(row=4,column=2)
Button(orderFrame,text="ORDERS",width=18,font=("Arial Black",10),command=position).grid(row=5,column=0)
Button(orderFrame,text="POSITION",width=18,font=("Arial Black",10),command=startThread).grid(row=5,column=1)
Button(orderFrame,text="STOP",width=18,font=("Arial Black",10),command=stopThread).grid(row=5,column=2)
profitLabel=Label(orderFrame,text="",width=18,font=("Arial Black",10))
profitLabel.grid(row=5,column=3)
positionFrame=Frame(root)
topFrame.config(background="black")
orderFrame.config(background="gray10")
positionFrame.config(background="gray20")
topFrame.pack()
orderFrame.pack()
positionFrame.pack()
root.mainloop()
REQUEST TOKEN
def popup():
    global top,entryToken
    top=Toplevel(root)
    entryToken=ttk.Entry(top)
    entryToken.grid(row=0,column=0)	
    Button(top,text="SUBMIT",command=connectZerodha).grid(row=0,column=1)
CONNECT TO ZERODHA
def connectZerodha():
    global kite
    kite=KiteConnect(api_key="")
    request_token=entryToken.get()
    data=kite.generate_session(request_token,api_secret="")
    kite.set_access_token(data["access_token"])
    top.destroy()
    username["text"]=(kite.profile()["user_name"])
GENERATE STOP LOSS AND QUANTITY
def generateFields():
    order_param_single = [{
        "exchange": "NSE",
        "tradingsymbol":name.get(),
        "transaction_type": "BUY",
        "variety": "CO",
        "product": "MIS",
        "order_type": "MARKET",
        "quantity": 1
        }]
    margin_detail = kite.order_margins(order_param_single)
    margin.delete(0,"end")
    margin.insert(0,margin_detail[0]["total"])
    qty=(int)((float)(capital.get())/margin_detail[0]["total"])
    quantity.delete(0,"end")
    quantity.insert(0,qty)
    sl=(float)(loss.get())/qty
    instruments="NSE:"+name.get()
    quotes=kite.quote(instruments)
    if(radio2.get()==1):
        sl=quotes["NSE:"+name.get()]["last_price"]-sl
    else:
        sl=quotes["NSE:"+name.get()]["last_price"]+sl 
    sl=(float)("{:.2f}".format(sl))
    sl=((int)(sl*100)-((int)(sl*100))%5)/100
    stoploss.delete(0,"end")
    stoploss.insert(0,sl)
    ltp.delete(0,"end")
    ltp.insert(0,quotes["NSE:"+name.get()]["last_price"])
PLACE ORDER
def placeOrder():
    stockSymbol=name.get()
    qty=(int)(quantity.get())
    sl=(float)(stoploss.get())
    orderType=kite.ORDER_TYPE_MARKET
    transType=kite.TRANSACTION_TYPE_BUY
    if(radio.get()==2):
        orderType=kite.ORDER_TYPE_LIMIT
    if(radio2.get()==2):
        transType=kite.TRANSACTION_TYPE_SELL
    limitPrice=(float)(ltp.get())
    kite.place_order(
    variety=kite.VARIETY_CO,
    exchange=kite.EXCHANGE_NSE,
    tradingsymbol=stockSymbol,
    transaction_type=transType,
    quantity=qty,
    product=kite.PRODUCT_MIS,
    order_type=orderType,
    validity=kite.VALIDITY_DAY,
    trigger_price=sl
    )
VIEW ORDER
def position():
    clearWidgets()
    orders=kite.orders()
    qty=0
    pnl=0
    avgPrice=0
    i=0
    for row in orders:
        if(row["status"]=="TRIGGER PENDING"):
            qty=row["quantity"]
            if(row["transaction_type"]=="BUY"):
                qty=-qty;
            avgPrice=averagePrice(row["parent_order_id"],orders)
            Label(positionFrame,text=row["order_id"],width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=0)
            Label(positionFrame,text=row["tradingsymbol"],width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=1)
            Label(positionFrame,text=qty,width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=2)
            Label(positionFrame,text=avgPrice,width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=3)
            Label(positionFrame,text="0",width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=4)
            Label(positionFrame,text="0",width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=5)
            Button(positionFrame,text="EXIT",width=10,bg="red",fg="white",font=("Arial Black",10),command=lambda:exitOrder(row["order_id"])).grid(row=i,column=6)
            i+=1
def averagePrice(parentid,order):
    for row in order:
        if((row["order_id"])==parentid):
            return row["average_price"]
SCAN  PROFIT AND LOSS(PNL)
def pnl():
    widgets=positionFrame.winfo_children()
    instruments=[]
    i=0
    
    while(i<(len(widgets))/7):
        instruments.append("NSE:"+widgets[i*7+1]["text"])
        i+=1
    avgPrice=0
    qty=0
    lastPrice=0
    
    i=0
    profit=0
    while(True):
        quote=(kite.quote(instruments)) 
        i=0
        overallProfit=0
        global stopPos
        if(stopPos==True):
            stopPos=False
            break
        widgetNum=0
        while(i<(len(widgets))/7):
            avgPrice=(float)(widgets[widgetNum+3]["text"])
            qty=(int)(widgets[widgetNum+2]["text"])
            lastPrice=quote[instruments[i]]["last_price"]
            profit=(lastPrice-avgPrice)*qty
            overallProfit+=profit
            widgets[widgetNum+5]["text"]="{:.2f}".format(profit)
            widgets[widgetNum+4]["text"]=lastPrice
            if(profit>0):
                widgets[widgetNum+5].config(fg="green")
            else:
                widgets[widgetNum+5].config(fg="red")
            i+=1
            widgetNum+=7
        profitLabel["text"]=overallProfit
        if(overallProfit>0):
            profitLabel.config(fg="green")
        else:
            profitLabel.config(fg="red")
REFRESH WIDGETS
def clearWidgets():
    widgets=positionFrame.winfo_children()
    for widget in widgets:
        widget.destroy()
EXIT ORDER
def exitOrder(order_id):
    kite.cancel_order(kite.VARIETY_CO, order_id, parent_order_id=None)
    stopThread()
    clearWidgets()
    position()
IMPLEMENT THREADS
def startThread():
    t1=threading.Thread(target=pnl)
    t1.start()
def stopThread():
    global stopPos
    stopPos=True
COMPLETE CODE
from tkinter import *
from tkinter import ttk
import sqlite3
import threading
from kiteconnect import KiteConnect
root=Tk()
root.geometry("670x200")
root.config(background="black")
style= ttk.Style()
style.theme_use('winnative')
stopPos=False
def generateFields():
    order_param_single = [{
        "exchange": "NSE",
        "tradingsymbol":name.get(),
        "transaction_type": "BUY",
        "variety": "CO",
        "product": "MIS",
        "order_type": "MARKET",
        "quantity": 1
        }]
    margin_detail = kite.order_margins(order_param_single)
    margin.delete(0,"end")
    margin.insert(0,margin_detail[0]["total"])
    qty=(int)((float)(capital.get())/margin_detail[0]["total"])
    quantity.delete(0,"end")
    quantity.insert(0,qty)
    sl=(float)(loss.get())/qty
    instruments="NSE:"+name.get()
    quotes=kite.quote(instruments)
    if(radio2.get()==1):
        sl=quotes["NSE:"+name.get()]["last_price"]-sl
    else:
        sl=quotes["NSE:"+name.get()]["last_price"]+sl 
    sl=(float)("{:.2f}".format(sl))
    sl=((int)(sl*100)-((int)(sl*100))%5)/100
    stoploss.delete(0,"end")
    stoploss.insert(0,sl)
    ltp.delete(0,"end")
    ltp.insert(0,quotes["NSE:"+name.get()]["last_price"])
def startThread():
    t1=threading.Thread(target=pnl)
    t1.start()
def stopThread():
    global stopPos
    stopPos=True
def connectZerodha():
    global kite
    kite=KiteConnect(api_key="")
    request_token=entryToken.get()
    data=kite.generate_session(request_token,api_secret="")
    kite.set_access_token(data["access_token"])
    top.destroy()
    username["text"]=(kite.profile()["user_name"])
def popup():
    global top,entryToken
    top=Toplevel(root)
    entryToken=ttk.Entry(top)
    entryToken.grid(row=0,column=0)	
    Button(top,text="SUBMIT",command=connectZerodha).grid(row=0,column=1)
def placeOrder():
    stockSymbol=name.get()
    qty=(int)(quantity.get())
    sl=(float)(stoploss.get())
    orderType=kite.ORDER_TYPE_MARKET
    transType=kite.TRANSACTION_TYPE_BUY
    if(radio.get()==2):
        orderType=kite.ORDER_TYPE_LIMIT
    if(radio2.get()==2):
        transType=kite.TRANSACTION_TYPE_SELL
    limitPrice=(float)(ltp.get())
    kite.place_order(
    variety=kite.VARIETY_CO,
    exchange=kite.EXCHANGE_NSE,
    tradingsymbol=stockSymbol,
    transaction_type=transType,
    quantity=qty,
    product=kite.PRODUCT_MIS,
    order_type=orderType,
    validity=kite.VALIDITY_DAY,
    trigger_price=sl
    )
def position():
    orders=kite.orders()
    qty=0
    pnl=0
    avgPrice=0
    i=0
    for row in orders:
        if(row["status"]=="TRIGGER PENDING"):
            qty=row["quantity"]
            if(row["transaction_type"]=="BUY"):
                qty=-qty;
            avgPrice=averagePrice(row["parent_order_id"],orders)
            Label(positionFrame,text=row["order_id"],width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=0)
            Label(positionFrame,text=row["tradingsymbol"],width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=1)
            Label(positionFrame,text=qty,width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=2)
            Label(positionFrame,text=avgPrice,width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=3)
            Label(positionFrame,text="0",width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=4)
            Label(positionFrame,text="0",width=10,bg="cornsilk3",fg="black",font=("Arial Black",10)).grid(row=i,column=5)
            Button(positionFrame,text="EXIT",width=10,bg="red",fg="white",font=("Arial Black",10),command=lambda:exitOrder(row["order_id"])).grid(row=i,column=6)
            i+=1
def averagePrice(parentid,order):
    for row in order:
        if((row["order_id"])==parentid):
            return row["average_price"]
    
def clearWidgets():
    widgets=positionFrame.winfo_children()
    for widget in widgets:
        widget.destroy()
def exitOrder(order_id):
    cancel_order(kite.VARIETY_CO, order_id, parent_order_id=None)
    stopThread()
    clearWidgets()
    position()
def pnl():
    widgets=positionFrame.winfo_children()
    instruments=[]
    i=0
    while(i<(len(widgets))/7):
        instruments.append("NSE:"+widgets[i+1]["text"])
        i+=7
    avgPrice=0
    qty=0
    lastPrice=0
    
    i=0
    profit=0
    while(True):
        quote=(kite.quote(instruments)) 
        i=0
        global stopPos
        if(stopPos==True):
            stopPos=False
            break
        while(i<(len(widgets))/7):
            avgPrice=(float)(widgets[i+3]["text"])
            qty=(int)(widgets[i+2]["text"])
            lastPrice=quote[instruments[(int)(i/7)]]["last_price"]
            profit=(lastPrice-avgPrice)*qty
            widgets[i+5]["text"]="{:.2f}".format(profit)
            widgets[i+4]["text"]=lastPrice
            if(profit>0):
                widgets[i+5].config(fg="green")
            else:
                widgets[i+5].config(fg="red")
            i+=7
topFrame=Frame(root)
Button(topFrame,text="CONNECT",command=popup,width=20,bg="green4",fg="white",font=("Arial Black",10)).grid(row=0,column=0)
username=Label(topFrame,width=20,font=("Arial Black",10))
username.grid(row=0,column=1)
Button(topFrame,text="SL&QUANTITY",command=generateFields,width=20,bg="green4",fg="white",font=("Arial Black",10)).grid(row=0,column=2)

orderFrame=Frame(root)
Label(orderFrame,text="NAME",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=0,column=0)
name=Entry(orderFrame,font=("Arial Black",10))
name.grid(row=0,column=1)
Label(orderFrame,text="MARGIN",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=0,column=2)
margin=Entry(orderFrame,font=("Arial Black",10))
margin.grid(row=0,column=3)
Label(orderFrame,text="CAPITAL",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=1,column=0)
capital=Entry(orderFrame,font=("Arial Black",10))
capital.grid(row=1,column=1)
Label(orderFrame,text="LOSS",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=1,column=2)
loss=Entry(orderFrame,font=("Arial Black",10))
loss.grid(row=1,column=3)
Label(orderFrame,text="QUANTITY",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=2,column=0)
quantity=Entry(orderFrame,font=("Arial Black",10))
quantity.grid(row=2,column=1)
Label(orderFrame,text="STOP LOSS",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=2,column=2)
stoploss=Entry(orderFrame,font=("Arial Black",10))
stoploss.grid(row=2,column=3)
radio = IntVar()  
R1 = Radiobutton(orderFrame,width=15, text="MARKET",bg="gray10",fg="white",font=("Arial Black",10),selectcolor='green', variable=radio,value=1)
R1.grid(row = 3, column = 0)
R2 = Radiobutton(orderFrame,width=15, text="LIMIT",bg="gray10",fg="white",font=("Arial Black",10), selectcolor='green',variable=radio,value=2)
R2.grid(row = 3, column = 1)
Label(orderFrame,text="LAST PRICE",width=20,bg="gray10",fg="white",font=("Arial Black",10)).grid(row=3,column=2)
ltp=Entry(orderFrame,font=("Arial Black",10))
ltp.grid(row=3,column=3)
radio2 = IntVar()  
R3 = Radiobutton(orderFrame,width=15, text="BUY",bg="gray10",fg="white",font=("Arial Black",10), selectcolor='green', variable=radio2,value=1)
R3.grid(row = 4, column = 0)
R4 = Radiobutton(orderFrame,width=15, text="SELL",bg="gray10",fg="white",font=("Arial Black",10), selectcolor='green', variable=radio2,value=2)
R4.grid(row = 4, column = 1)
Button(orderFrame,text="PLACE ORDER",width=18,bg="green4",fg="white",font=("Arial Black",10),command=placeOrder).grid(row=4,column=2)
Button(orderFrame,text="ORDERS",width=18,font=("Arial Black",10),command=position).grid(row=5,column=0)
Button(orderFrame,text="POSITION",width=18,font=("Arial Black",10),command=startThread).grid(row=5,column=1)
Button(orderFrame,text="STOP",width=18,font=("Arial Black",10),command=stopThread).grid(row=5,column=2)
positionFrame=Frame(root)
topFrame.config(background="black")
orderFrame.config(background="gray10")
positionFrame.config(background="gray20")
topFrame.pack()
orderFrame.pack()
positionFrame.pack()
root.mainloop()

