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
collection = db.Transaction

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
    def Confirm():
        st.session_state.confirm = True

    if(st.button("CONFIRM",on_click=Confirm,key=10) or st.session_state.confirm):
        record = collection.insert_one(item)


        
