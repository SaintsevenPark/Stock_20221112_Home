import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import time
import numpy as np
import pandas_ta as pt
import mplfinance as mpf

from plotly.subplots import make_subplots
#
from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst


# -------------------- 페이지 형태 최기화
st.set_page_config(page_title=None, page_icon="chart_with_upwards_trend", layout="wide", initial_sidebar_state="auto", menu_items=None)

l_line = 2
s_line = -10
stock_count = 300
default_strategy = 8
start_year = '2022'

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
df_stocklistfile = pd.read_csv('stocklist_krx.csv')
df_stocklist['index'] = df_stocklistfile[0:stock_count].index
df_stocklist['Code'] = df_stocklistfile[0:stock_count]['Code']
df_stocklist['Name'] = df_stocklistfile[0:stock_count]['Name']
df_stocklist['Close'] = df_stocklistfile[0:stock_count]['Close']

st.sidebar.markdown("## KRX")
selected_strategy = st.sidebar.selectbox("전략 선택", strategy_names_to_funcs.keys(), index=default_strategy)

number = st.sidebar.number_input('Insert a number', min_value=0, max_value=stock_count)

tick_code = df_stocklist['Code'].iloc[number]
df_origin = fdr.DataReader(tick_code, start=start_year)
df_heiken = ssl.heikin_ashi(df_origin).astype(int)
df_squeeze = ssl.get_squeeze_momentum(df_origin)

# -----------------------------------------------------------------------
with st.expander("순수 데이터 프레임"):
    st.dataframe(df_origin)
with st.expander("Heiken Ashi 데이터 프레임"):
    st.dataframe(df_heiken)
with st.expander("Squeeze 데이터 프레임"):
    st.dataframe(df_squeeze)

df = ssl.get_indicator(df_origin, l_line, s_line)
with st.expander("모든 지표"):
    st.dataframe(df)
# -----------------------------------------------------------------------

stock_code = df_stocklist['Code'].iloc[number]
stock_name = df_stocklist['Name'].iloc[number]
stock_price = df['Close'].iloc[-1]

st.sidebar.markdown(f"### [{stock_code}] {stock_name} : {stock_price}")
with st.sidebar.expander("주식 목록"):
    st.dataframe(df_stocklist)

# ====================   전략 선택 매수 마킹 ===========================
Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_strategy](df)
st.write(desc)


# MatPlotlib에서 마킹하기 위해 df 가공함
df['Buy'] = np.nan
for i in Buy:
    df['Buy'].iloc[i] = df['Close'].iloc[i]

df['Sell'] = np.nan
for i in Sell:
    df['Sell'].iloc[i] = df['Close'].iloc[i]


# # -----------------------  Matplotlib 시작
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize = (30,25))
ax1 = plt.subplot(4, 1, 1)
plt.plot(df['Close'], linewidth = 1, label = 'CLOSING PRICE')
plt.plot(df['SUPERTl'], linewidth = 0.5, label = 'SUPER TRENDl')
# plt.plot(df['SUPERTlp'], linewidth = 1, label = 'SUPER TRENDl %')
plt.plot(df['SUPERTs'], linewidth = 0.5, label = 'SUPER TRENDs')
# plt.plot(df['SUPERTsp'], linewidth = 1, label = 'SUPER TRENDs %')
plt.plot(df['EMA200'], linewidth = 1, label = 'EMA200')
plt.plot(df.index, df['Buy'], marker='^', color='r', markersize=10, linewidth=0, label='BUY SIGNAL')
# plt.plot(df.index, df['Sell'], marker='v', color='green', markersize=10, linewidth=0, label='Sell SIGNAL')

plt.fill_between(df.index, df['SUPERTl'], df['SUPERTlp'], color='r', alpha=0.1)
plt.fill_between(df.index, df['SUPERTs'], df['SUPERTsp'], color='b', alpha=0.1)
plt.title("Super Trend")
plt.legend(loc = 'best')
# plt.axis('off')

ax2 = plt.subplot(4, 1, 2, sharex=ax1)
plt.plot(df['STOCHRSIk'], linewidth = 1, label = 'STOCHRSIk')
plt.plot(df['STOCHRSId'], linewidth = 1, label = 'STOCHRSId')
plt.plot(df.index, (df['Buy'] * 0) + df['STOCHRSIk'] , marker='^', color='r', markersize=10, linewidth=0, label='BUY SIGNAL')
plt.axhline(y=20, color='red', linewidth=0.8, linestyle='--')
plt.title('Stochastic RSI')
plt.legend(loc = 'best')
plt.subplots_adjust(wspace=.025, hspace=0.2)

ax3 = plt.subplot(4, 1, 3, sharex=ax1)
plt.plot(df['Close'], linewidth = 1, label = 'CLOSE')
plt.plot(df['SMA5'], linewidth = 1, label = 'SMA 5')
plt.plot(df['SMA20'], linewidth = 1, label = 'SMA 20')
plt.plot(df.index, df['Buy'], marker='^', color='r', markersize=10, linewidth=0, label='BUY SIGNAL')
plt.title('SMA 5-20 X')
plt.legend(loc = 'best')
plt.subplots_adjust(wspace=.025, hspace=0.2)

ax4 = plt.subplot(4, 1, 4, sharex=ax1)
plt.plot(df['Close'], linewidth = 1, label = 'CLOSE')
# plt.plot(df['BBL'], linewidth = 0.5, label = 'BBL', linestyle='--')
# plt.plot(df['BBM'], linewidth = 0.5, label = 'BBM')
plt.fill_between(df.index, df['BBL'], df['BBM'], color='r', alpha=0.1)
# plt.plot(df['BBU'], linewidth = 0.5, label = 'BBU')
plt.fill_between(df.index, df['BBU'], df['BBM'], color='green', alpha=0.1)
plt.plot(df.index, df['Buy'], marker='^', color='r', markersize=10, linewidth=0, label='BUY SIGNAL')
plt.title('Bollinger Band')
plt.legend(loc = 'best')
plt.subplots_adjust(wspace=.025, hspace=0.2)


st.pyplot()

# -----------------------  Heiken Ashi  Matplotlib 시작
ohcl_heiken = df_heiken[['Open', 'High', 'Close', 'Low']]
ohcl_heiken = ohcl_heiken.astype(int)
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(30, 15))

mpf.plot(ohcl_heiken,
         volume_panel=2,
         figratio=(3, 1),
         figscale=2,
         style='charles',
         type='candle',
         returnfig=True)

st.pyplot()

# -----------------------  Squeeze Momentum  Matplotlib 시작
ohcl_squeeze = df_squeeze[['Open', 'High', 'Close', 'Low']]

colors = []

for ind, val in enumerate(df_squeeze['value']):
    if val >= 0:
        color = 'green'
        if val > df_squeeze['value'][ind - 1]:
            color = 'lime'
    else:
        color = 'maroon'
        if val < df_squeeze['value'][ind - 1]:
            color = 'red'
    colors.append(color)

st.set_option('deprecation.showPyplotGlobalUse', False)
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(30, 15))

apds = [mpf.make_addplot(df_squeeze['value'], panel=1, type='bar', color=colors, alpha=0.5, secondary_y=False),
        mpf.make_addplot([0] * len(df_squeeze), panel=1, type='scatter', marker='x', markersize=80,
                         color=['green' if s else 'red' for s in df_squeeze['squeeze_off']], secondary_y=False),
        ]

mpf.plot(ohcl_squeeze,
         volume_panel=2,
         figratio=(3, 1),
         figscale=1.5,
         style='charles',
         type='candle',
         addplot=apds,
         returnfig=True)

st.pyplot()


