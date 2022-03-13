# -*- coding: utf-8 -*-
"""
Created on 09 Juin 16:02
@author: Hajjar
"""
import seaborn as sns
from sklearn.utils import shuffle
import tornado.ioloop
import tornado.web
import tornado.options
import streamlit as st
import pymongo
from pymongo import MongoClient
import numpy as np
import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import altair as alt
from random import randint
import time
import os
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Trade Change live')


#alt.renderers.set_embed_options(scaleFactor=1)

st.title("IA TRADING BINANCE DELTACHANGE")
st.markdown(
    "*TRADECHANGEDELTA est une intelligence artificielle en cours de teste réel sur les cours du marché BAT token,* "
    "*il est complètement autonome et effectue c'est prédiction du marché chaque seconde en haute fréquence* "
    "*,mais cependant la stratégie qu'elle suit l'empêchée d'effectuer du trading à haute fréquence (les frais de Binance me feront perdre mes gains) :°* "
    "* sur le graphique ci-dessous vous pouvez voir les cours du marché réel et les prédictions faite par l'IA* "
    "* il calcule lui-même sont propres Stoploss pour son profit en cas de chute brutal du marché.* "
)
#st.sidebar.title("Control Panel")





#@st.cache
def load_data():
    client = pymongo.MongoClient("mongodb+srv://killia:Mhajjar3@cluster0.w4eru.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.mydatabase
    col = db.customersw
    data = pd.DataFrame(list(col.find()))
    data = data.drop(columns=["_id","created_time"])
    data = data.dropna()
    #data =  shuffle(data, random_state=42)
    #data = data.iloc[-1000]
    # Convert integer valued (numeric) columns to floating point
    numeric_columns = data.select_dtypes(["int64", "float64"]).columns
    data[numeric_columns] = data[numeric_columns].astype("float32")
    #data = pd.read_csv('transaction_simplon.csv', nrows=nrows)
    return data

#int_val = st.slider('Choix dunombre de donné visualisé en live', min_value=100, max_value=1000, value=200, step=1)
#int_val = st.number_input(' Choix du nombre de donné visualisé en live', min_value=10, max_value=15000, value=500, step=1)

transaction = load_data()
x = transaction
#int_val = st.number_input(' Choix du nombre de donné visualisé en live', min_value=100, max_value=15000, value=x.iloc[-1], step=1)
#print(x)
signale_achat = x[x.ref == 1]
signale_vente = x[x.ref == 2]
signale_stoploss = x[x.ref == 3]
USDT = x.totoUSDT
USDT = USDT.iloc[-1]
gain = x.gain.sum()
perte = x.perte.sum()
benefice = gain - perte
#print(USDT)
BAT = x.totoBAT
BAT = BAT.iloc[-1]
#print(BAT)
prix = x.prix
prix = prix.iloc[-1]

import plotly.offline as py
import plotly.graph_objs as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=x.index, y=x['prix'], name='cours BAT'))
fig.add_trace(go.Scatter(x=x.index, y=x['predict'], name='prediction IA'))
fig.add_trace(go.Scatter(x=x.index, y=x['predictUpper'], name='prediction UpperBand IA'))
fig.add_trace(go.Scatter(x=x.index, y=x['upperband'], name='UpperBand'))
fig.add_trace(go.Scatter(x=x.index, y=x['predictLower'], name='prediction LowerBand IA'))
fig.add_trace(go.Scatter(x=x.index, y=x['lowerband'], name='LowerBand'))
fig.add_trace(go.Scatter(x=signale_achat.index, y=signale_achat.prix, mode='markers', name='achat'))
fig.add_trace(go.Scatter(x=signale_vente.index, y=signale_vente.prix, mode='markers', name='vente'))
fig.add_trace(go.Scatter(x=signale_stoploss.index, y=signale_stoploss.prix, mode='markers', name='stoploss'))
#fig.update_layout(showlegend=True, title='BAT')
fig.update_layout(
    title="<b> Live Trade IA </b>")



#fig.show()
st.plotly_chart(fig)

#st.sidebar.title("Control Panel")
st.write("USDT EN POSSESSION",round(float(USDT),3))
st.write("TOTAL DES BAT EN DOLLARS EN COURS DE TRADE",round(float(BAT),3))
st.write("Prix actuelle des cours du marché BAT",round(float(prix),3))
st.write("Gain Rapporter par l'IA",round(float(gain),3))
st.write("Pertes Stoploss",round(float(perte),3))
st.write("Benefice",round(float(benefice),3))


import streamlit as st
from streamlit_autorefresh import st_autorefresh

# update every 5 mins
st_autorefresh(interval=1 * 60 * 1000, key="dataframerefresh")

#def refresher(seconds):
    #while True:
        #mainDir = os.path.dirname(__file__)
        #filePath = os.path.join(mainDir, 'app.py')
        #with open(filePath, 'w') as f:
            #f.write(f'# {randint(0, 10000)}')
        #time.sleep(seconds)

#refresher(20)
#st.sidebar.title("Control Panel")
#right_col = st.beta_columns(1)

#right_col.markdown(f"**USDT DOLLARS:** {float(USDT):,}")
#right_col.markdown(f"** BAT TRANSAC DOLLARS :** {float(BAT):.4f}")
#right_col.markdown(f"** BAT prix du marché en cours :** {float(prix):.4f}")
#right_col.markdown(
    #f"**80% credible region for click rate:** [{posterior.ppf(0.1):.4f}, {posterior.ppf(0.9):.4f}]"
#)
#right_col.markdown(
#    f"**P(click rate < than critical threshold):** {worst_case_proba:.2%}"
#)
#right_col.subheader(f"***Final decision:*** {decision} :{emoji}:")
