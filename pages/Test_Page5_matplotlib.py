import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import time
import numpy as np
import pandas_ta as pt

from plotly.subplots import make_subplots
#
from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst


l_line = 2
s_line = -10
stock_count = 100
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
df_stocklistfile = pd.read_csv('stocklist_krx.csv')
df_stocklist['index'] = df_stocklistfile[0:stock_count].index
df_stocklist['Code'] = df_stocklistfile[0:stock_count]['Code']
df_stocklist['Name'] = df_stocklistfile[0:stock_count]['Name']
df_stocklist['Close'] = df_stocklistfile[0:stock_count]['Close']

st.sidebar.markdown("## KRX")
selected_strategy = st.sidebar.selectbox("전략 선택", strategy_names_to_funcs.keys(), index=default_strategy)

number = st.sidebar.number_input('Insert a number', min_value=0, max_value=stock_count)

tick_code = df_stocklist['Code'].iloc[number]
df = fdr.DataReader(tick_code, '2022')
df = ssl.get_indicator(df)
stock_code = df_stocklist['Code'].iloc[number]
stock_name = df_stocklist['Name'].iloc[number]
stock_price = df['Close'].iloc[-1]

st.sidebar.markdown(f"### [{stock_code}] {stock_name} : {stock_price}")
with st.sidebar.expander("주식 목록"):
    st.dataframe(df_stocklist)

# ====================   전략 선택 매수 마킹 ===========================
if selected_strategy == 'Strategy 9' or selected_strategy == 'Strategy 10' or selected_strategy == 'Strategy 11':
    Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_strategy](df, l_line, s_line)
    st.write(desc)
else:
    Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_strategy](df)
    st.write(desc)


# MatPlotlib에서 마킹하기 위해 df 가공함
df['Buy'] = np.nan
for i in Buy:
    df['Buy'].iloc[i] = df['Close'].iloc[i]

# # -----------------------  Matplotlib 시작
df['SUPERlp'] = df['SUPERTl'] *  (1 + (l_line / 100))
df['SUPERsp'] = df['SUPERTs'] *  (1 + (s_line / 100))
#
# plt.style.use('fivethirtyeight')
# plt.rcParams['figure.figsize'] = (24, 6)
#
# # fig, ax = plt.subplots(figsize=(12,3))
# fig, ax = plt.subplots()
# ax = plt.plot(df['Close'], linewidth = 1, label = 'CLOSING PRICE')
# ax = plt.plot(df['SUPERTl'], linewidth = 1, label = 'SUPER TRENDl')
# ax = plt.plot(df['SUPERTlp'], linewidth = 1, label = 'SUPER TRENDl %')
# ax = plt.plot(df['SUPERTs'], linewidth = 1, label = 'SUPER TRENDs')
# ax = plt.plot(df['SUPERTsp'], linewidth = 1, label = 'SUPER TRENDs %')
# ax = plt.plot(df.index, df['Buy'], marker='^', color='r', markersize=10, linewidth=0, label='BUY SIGNAL')
# ax = plt.title(f"[{stock_code}] {stock_name} : {stock_price}")
# ax = plt.legend(loc = 'best')
#
# st.pyplot(fig, clear_figure=True)
#
# fig, ax = plt.subplots()
# ax = plt.plot(df['STOCHRSIk'], linewidth = 1, label = 'CLOSING PRICE')
# ax = plt.plot(df['STOCHRSId'], linewidth = 1, label = 'SUPER TRENDl')
# # ax = plt.plot(df.index, df['Buy'], marker='^', color='r', markersize=10, linewidth=0, label='BUY SIGNAL')
# ax = plt.title(f"[{stock_code}] {stock_name} : {stock_price}")
# ax = plt.legend(loc = 'best')
#
# st.pyplot(fig, clear_figure=True)

# # -----------------------  Matplotlib 시작 다른 방법
plt.style.use('fivethirtyeight')
# plt.rcParams['figure.figsize'] = (24, 6)
fig = plt.figure(figsize = (24,12))
plt.subplot(2, 1, 1)
plt.plot(df['Close'], linewidth = 1, label = 'CLOSING PRICE')
plt.plot(df['SUPERTl'], linewidth = 1, label = 'SUPER TRENDl')
# plt.plot(df['SUPERTlp'], linewidth = 1, label = 'SUPER TRENDl %')
plt.plot(df['SUPERTs'], linewidth = 1, label = 'SUPER TRENDs')
# plt.plot(df['SUPERTsp'], linewidth = 1, label = 'SUPER TRENDs %')
plt.plot(df.index, df['Buy'], marker='^', color='r', markersize=10, linewidth=0, label='BUY SIGNAL')
plt.title(f"[{stock_code}] {stock_name} : {stock_price}")
plt.legend(loc = 'best')
# plt.axis('off')
plt.subplot(2, 1, 2)
plt.plot(df['STOCHRSIk'], linewidth = 1, label = 'STOCHRSIk')
plt.plot(df['STOCHRSId'], linewidth = 1, label = 'STOCHRSId')
plt.legend(loc = 'best')
plt.subplots_adjust(wspace=.025, hspace=.05)
st.pyplot(fig)
