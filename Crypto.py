import streamlit as st
import pandas as pd
import numpy as np
import requests
from time import sleep
import smtplib
from PIL import Image
import pymongo
from datetime import datetime
import pytz
import time
from collections import defaultdict

image = Image.open("D:/HTML CODES/logo.jpg")

st.markdown('''# ****MY CRYPTOCURRENCY PORTFOLIO****
Manage all your Crypto Inventory here''')


st.image(image)

df = pd.read_json("https://api.coindcx.com/exchange/ticker")

@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

#client = init_connection()
client = pymongo.MongoClient("mongodb+srv://sakshith2002:admin@cluster0.frpdmtc.mongodb.net/?retryWrites=true&w=majority")
db = client.MyDB
collection1 = db.Transaction
collection2 = db.Portfolio

def round_value(input_value):
    Input=input_value.values
    val = int(float(Input[0]))
    if val > 1:
        a = float(round(val, 2))
    else:
        a = float(round(val, 8))
    return a
    
col1, col2, col3 = st.columns(3)

col1_selection = st.sidebar.selectbox('Price 1', df.market, list(df.market).index('BTCINR'))
col2_selection = st.sidebar.selectbox('Price 2', df.market, list(df.market).index('ETHINR'))
col3_selection = st.sidebar.selectbox('Price 3', df.market, list(df.market).index('GALAINR'))
col4_selection = st.sidebar.selectbox('Price 4', df.market, list(df.market).index('DOGEBUSD') )
col5_selection = st.sidebar.selectbox('Price 5', df.market, list(df.market).index('SHIBBUSD') )
col6_selection = st.sidebar.selectbox('Price 6', df.market, list(df.market).index('PHBBTC') )
col7_selection = st.sidebar.selectbox('Price 7', df.market, list(df.market).index('SOLINR') )
col8_selection = st.sidebar.selectbox('Price 8', df.market, list(df.market).index('ATOMINR') )
col9_selection = st.sidebar.selectbox('Price 9', df.market, list(df.market).index('BUSDINR') )

col1_df = df[df.market == col1_selection]
col2_df = df[df.market == col2_selection]
col3_df = df[df.market == col3_selection]
col4_df = df[df.market == col4_selection]
col5_df = df[df.market == col5_selection]
col6_df = df[df.market == col6_selection]
col7_df = df[df.market == col7_selection]
col8_df = df[df.market == col8_selection]
col9_df = df[df.market == col9_selection]

col1_price = round_value(col1_df.bid)
col2_price = round_value(col2_df.bid)
col3_price = round_value(col3_df.bid)
col4_price = round_value(col4_df.bid)
col5_price = round_value(col5_df.bid)
col6_price = round_value(col6_df.bid)
col7_price = round_value(col7_df.bid)
col8_price = round_value(col8_df.bid)
col9_price = round_value(col9_df.bid)


col1_percent = f'{float(col1_df.change_24_hour)}%'
col2_percent = f'{float(col2_df.change_24_hour)}%'
col3_percent = f'{float(col3_df.change_24_hour)}%'
col4_percent = f'{float(col4_df.change_24_hour)}%'
col5_percent = f'{float(col5_df.change_24_hour)}%'
col6_percent = f'{float(col6_df.change_24_hour)}%'
col7_percent = f'{float(col7_df.change_24_hour)}%'
col8_percent = f'{float(col8_df.change_24_hour)}%'
col9_percent = f'{float(col9_df.change_24_hour)}%'

col1.metric(col1_selection, col1_price, col1_percent)
col2.metric(col2_selection, col2_price, col2_percent)
col3.metric(col3_selection, col3_price, col3_percent)
col1.metric(col4_selection, col4_price, col4_percent)
col2.metric(col5_selection, col5_price, col5_percent)
col3.metric(col6_selection, col6_price, col6_percent)
col1.metric(col7_selection, col7_price, col7_percent)
col2.metric(col8_selection, col8_price, col8_percent)
col3.metric(col9_selection, col9_price, col9_percent)

if "Click" not in st.session_state:
    st.session_state.Click = False

def callback():
    st.session_state.Click = True

def get_portfolio():
    get_pf = client.MyDB
    get_item = get_pf.Portfolio.find() 
    get_item = list(get_item)
    return get_item

st.session_state.get_pf = get_portfolio()
st.session_state.get_pf_init = st.session_state.get_pf
st.session_state.myquery_cost = {"Portfolio_Cost": st.session_state.get_pf[0]['Portfolio_Cost']}
st.session_state.myquery_value = {"Portfolio_Value": st.session_state.get_pf[0]['Portfolio_Value']}
st.session_state.myquery_gain = {"Absolute_Gain_Loss": st.session_state.get_pf[0]['Absolute_Gain_Loss']} 
st.session_state.myquery_pct = {"Gain_Loss_Pctg": st.session_state.get_pf[0]['Gain_Loss_Pctg']}


def Update_portfolio():
    for i in range(len(st.session_state.get_item)-1,len(st.session_state.get_item)):
        if(len(st.session_state.get_item)==0):
            break
        else: 
            if(st.session_state.get_item[-1]['TYPE']==1):
                st.session_state.get_pf[0]['Portfolio_Cost'] = st.session_state.get_pf[0]['Portfolio_Cost'] + st.session_state.get_item[-1]['AMOUNT']
            if(st.session_state.get_item[-1]['TYPE']==2):
                st.session_state.get_pf[0]['Portfolio_Cost'] = st.session_state.get_pf[0]['Portfolio_Cost'] - st.session_state.get_item[-1]['AMOUNT']
    
    return st.session_state.get_pf[0]['Portfolio_Cost']

if "confirm" not in st.session_state:
    st.session_state.confirm=False
if "rollup_confirm" not in st.session_state:
    st.session_state.rollup_confirm=False
if "rollup_value" not in st.session_state:
    st.session_state.rollup_value = False
if "rollup_gain" not in st.session_state:
    st.session_state.rollup_gain = False
if "rollup_pct" not in st.session_state:
    st.session_state.rollup_pct = False
def Updated():
    st.session_state.confirm=True
    st.session_state.Click = False
    if(st.session_state.confirm==True):
        collection1.insert_one(item)
        st.session_state.rollup_confirm=True
        st.session_state.rollup_value = True
        st.session_state.rollup_gain = True
        st.session_state.rollup_pct = True
        st.session_state.confirm = False


if (st.button("Click here to add new transaction",key = 1, on_click=callback) or st.session_state.Click):
    name = st.text_input("Name of the Coin",key=2,placeholder="Name of the coin. Ex:'Ethereum'") 
    st.session_state.Name=name
    symbol = st.text_input("Symbol of the Coin",key=3,placeholder="Ex:'ETH'")
    st.session_state.Symbol=symbol
    def Purchase():
        st.session_state.Type=1

    def Sell():
        st.session_state.Type=0
   
    Options = ['Purchase','Sell']
    type = st.radio("Select",on_change=Purchase,key=4,options=Options)
    if(type=="Purchase"):
        Purchase()
    else:
        Sell()
    amount = st.number_input("Total amount spent",key=5)
    st.session_state.Amount=amount
    price_purchased_at = st.number_input("Price purchased at",key=6)
    st.session_state.Price_p_at=price_purchased_at
    date_of_transaction=st.date_input("Date of transaction",key=7)
    t = st.session_state.Date_of_transaction=date_of_transaction 
    st.session_state.No_of_coins = st.number_input("Number of coins",key=8)
    
    tz = pytz.timezone("Asia/Kolkata")
    new_date = t.strftime('%m/%d/%Y')

    item = {
        "NAME": st.session_state.Name,
        "SYMBOL": st.session_state.Symbol,
        "TYPE": st.session_state.Type,
        "AMOUNT": st.session_state.Amount,
        "PRICE_PURCHASED_AT":st.session_state.Price_p_at,
        "DATE_OF_TRANSACTION":new_date,
        "NO_OF_COINS":st.session_state.No_of_coins
    }
    st.session_state.Item = item
    
    if "confirm" not in st.session_state:
        st.session_state.confirm = False
    
    
    st.button("CONFIRM",on_click=Updated,key=10)

def get_data():
    get_db = client.MyDB
    get_item = get_db.Transaction.find()
    get_item = list(get_item)
    return get_item

st.session_state.get_item = get_data()

#st.session_state.portfolio ={
#    "Portfolio_Cost": 0,
#    "Portfolio_Value": 0,
#    "Absolute_Gain_Loss": 0,
#    "Gain_Loss_Pctg": 0
#}
#record2 = collection2.insert_one(st.session_state.portfolio)
st.session_state.flag=1
def Roll_up(process):
    if(process==1):
        st.session_state.updated = {"$set": {"Portfolio_Cost": st.session_state.Updated_value}}
        collection2.update_one(st.session_state.myquery_cost,st.session_state.updated)
    if(process==2):
        st.session_state.updated = {"$set": {"Portfolio_Value": st.session_state.total_live_price}}
        collection2.update_one(st.session_state.myquery_value,st.session_state.updated)
    if(process==3):
        st.session_state.updated = {"$set": {"Absolute_Gain_Loss": st.session_state.gain_loss}}
        collection2.update_one(st.session_state.myquery_gain,st.session_state.updated)
    if(process==4):
        st.session_state.updated = {"$set": {"Gain_Loss_Pctg": st.session_state.percent}}
        collection2.update_one(st.session_state.myquery_pct,st.session_state.updated)
if(st.session_state.rollup_confirm==True):
    st.session_state.Updated_value = Update_portfolio()
    run1 = Roll_up(1) 
    if(run1):
        st.session_state.flag = st.session_state.flag + 1
    st.session_state.rollup_confirm=False
 
def get_symbol():
    list_of_symbol = []
    for i in st.session_state.get_item:
        list_of_symbol.append(i['SYMBOL'])
    return list_of_symbol
st.session_state.list_of_symbols = get_symbol()

#print(df.market)
st.session_state.total_live_price = 0
for i in range(len(st.session_state.get_item)):
    if(len(st.session_state.get_item)==0):
            break
    else:
         st.session_state.list_prices_indexes = list(df.market)
st.session_state.index_of_coins = []
for k in st.session_state.list_of_symbols:
    for j in st.session_state.list_prices_indexes:
        if(k==j):
            index = list(df.market).index(k)
            st.session_state.index_of_coins.append(index)

st.session_state.list_of_prices = []
st.session_state.d={}
for z in st.session_state.index_of_coins:
    price = df[['bid']].iloc[z]
    sym = df[['market']].iloc[z]
    s = str(sym[0])
    no_of_coin = 0 
    if (s not in st.session_state.d.keys()):
        st.session_state.d[s]=0
    if(st.session_state.d[s]==1):
        pass
    elif(st.session_state.d[s] == 0):
        for f in st.session_state.get_item:
            if(f['SYMBOL']==s):
                no_of_coin = no_of_coin + f['NO_OF_COINS']
                st.session_state.d[s]=1
        price_value = no_of_coin * float(price[0])   
    #for k,v in st.session_state.d.items():
    #    print(k," : ",v)
    #print("n",no_of_coin," : ", s)
        st.session_state.list_of_prices.append(price_value)
    
    
st.session_state.prices = list(st.session_state.list_of_prices)

for i in range(len(st.session_state.prices)):
    st.session_state.total_live_price = st.session_state.total_live_price + float(st.session_state.prices[i]) 

st.session_state.total_live_price = st.session_state.total_live_price 
if(st.session_state.rollup_value==True):
    run2 = Roll_up(2)
    
st.session_state.gain_loss =  st.session_state.get_pf[0]['Portfolio_Value'] - st.session_state.get_pf[0]['Portfolio_Cost']

if "f" not in st.session_state:
    st.session_state.f = False
if(st.session_state.rollup_gain==True):
    run3 = Roll_up(3) 
    st.session_state.f = True


if(st.session_state.f):
    try:
        st.session_state.gain_loss =  st.session_state.get_pf[0]['Portfolio_Value'] - st.session_state.get_pf[0]['Portfolio_Cost']
        st.session_state.percent = (st.session_state.gain_loss*100)/st.session_state.get_pf[0]['Portfolio_Cost']
        st.session_state.percent = st.session_state.percent/100
        st.session_state.percent = "{:.0%}".format(st.session_state.percent)
    except ZeroDivisionError as er:
        pass 

    if(st.session_state.rollup_pct==True):
        run4 = Roll_up(4)
        
 
    
       
