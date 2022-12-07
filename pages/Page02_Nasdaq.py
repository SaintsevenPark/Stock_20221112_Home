import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import time
import numpy as np
import cufflinks as cf
# # https://lumiamitie.github.io/python/cufflinks_basic/ Cufflinks 참조
# # import plotly.offline as plyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as pt
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst


# -------------------- 페이지 형태 초기화
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

l_line = 2
s_line = -10
stock_length = 100
start_year = '2022'
default_strategy = 10

strategy_names_to_funcs = {
    "Strategy 1": sst.strategy01,
    "Strategy 2": sst.strategy02,
    "Strategy 3": sst.strategy03,
    "Strategy 4": sst.strategy04,
    "Strategy 5": sst.strategy05,
    "Strategy 6": sst.strategy06,
    "Strategy 7": sst.strategy07,
    "Strategy 8": sst.strategy08,
    "Strategy 9": sst.strategy09,
    "Strategy 10": sst.strategy10,
    "Strategy 11": sst.strategy11,
}

df_stocklist = pd.DataFrame()
# 새로 읽어올때만 실행
# df = fdr.StockListing('NASDAQ')
# df.to_csv('stocklist_nasdaq.csv')
df_stocklistfile = pd.read_csv('stocklist_nasdaq.csv')

df_stocklist['index'] = df_stocklistfile[0:stock_length].index
df_stocklist['Symbol'] = df_stocklistfile[0:stock_length]['Symbol']
df_stocklist['Name'] = df_stocklistfile[0:stock_length]['Name']
# st.dataframe(df)


st.sidebar.markdown("## NASDAQ")
selected_strategy = st.sidebar.selectbox("전략 선택", strategy_names_to_funcs.keys(), index=default_strategy)


number = st.sidebar.number_input('Insert a number', min_value=0, max_value=stock_length)

tick_code = df_stocklist['Symbol'].iloc[number]
df = fdr.DataReader(tick_code, start=start_year)
df = ssl.get_indicator(df, l_line, s_line)
stock_code = df_stocklist['Symbol'].iloc[number]
stock_name = df_stocklist['Name'].iloc[number]
stock_price = df['Close'].iloc[-1]

st.sidebar.markdown(f"### [{stock_code}] {stock_name} : {stock_price}")
with st.sidebar.expander("주식 목록"):
    st.dataframe(df_stocklist)


# ====================   전략 선택 매수 마킹 ===========================
Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_strategy](df)
st.write(desc)

# ----------------------------------
fig = df[['Close', 'SUPERTl', 'SUPERTs']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="일간 가격 변동")
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)

# STOCHASTICRSI
fig = df[['STOCHRSIk', 'STOCHRSId']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="STOCHASTIC RSI", theme='white')
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
fig.add_hline(y=20, line=dict(width=1, color='red', dash='dash'))
st.plotly_chart(fig)

# 이동평균선
fig = df[['Close', 'SMA5', 'SMA20']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="이동평균선 5와 20 교차")
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)
# Super Trend
fig = df[['Close', 'SUPERTl', 'SUPERTs']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="Super Trend", theme="space")
for i in range(len(superBuy)):
    fig.add_vline(x=df.iloc[superBuy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(superSell)):
    fig.add_vline(x=df.iloc[superSell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)
# 볼린저밴드
fig = df[['Close', 'BBL', 'BBU']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="볼린저 밴드")
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)
# RSI
fig = df['RSI'].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="RSI")
fig.add_hline(y=30, line=dict(width=1, color='pink', dash='dash'))
fig.add_hline(y=70, line=dict(width=1, color='cyan', dash='dash'))
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)
# MFI
fig = df['MFI'].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="MFI")
fig.add_hline(y=30, line=dict(width=1, color='pink', dash='dash'))
fig.add_hline(y=70, line=dict(width=1, color='cyan', dash='dash'))
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)
# MACD
fig = df[['MACD', 'MACDs']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="MACD")
fig.add_hline(y=0, line=dict(width=1, color='pink', dash='dash'))
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)
# CCI
fig = df['CCI'].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="CCI")
fig.add_hline(y=100, line=dict(width=1, color='pink', dash='dash'))
fig.add_hline(y=-100, line=dict(width=1, color='cyan', dash='dash'))
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)

# TRIX
fig = df[['TRIX', 'TRIXs']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="TRIX")
fig.add_hline(y=0, line=dict(width=2, color='pink', dash='dash'))
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)



