import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import numpy as np
import mplfinance as mpf

from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst

# **************************** 변수 초기화
l_line = 2
s_line = -10
stock_count = 300
default_strategy = 8

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
df_pure = fdr.DataReader(tick_code, '2022')
df_all = ssl.get_indicator(df_pure, l_line, s_line)
stock_code = df_stocklist['Code'].iloc[number]
stock_name = df_stocklist['Name'].iloc[number]
stock_price = df_pure['Close'].iloc[-1]

# Squeeze Momentum
df_squeeze = ssl.get_squeeze_momentum(df_pure)

st.sidebar.markdown(f"### [{stock_code}] {stock_name} : {stock_price}")
with st.sidebar.expander("주식 목록"):
    st.dataframe(df_stocklist)

# ====================   전략 선택 매수 마킹 ===========================
Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_strategy](df_all)
st.write(desc)


# MatPlotlib에서 마킹하기 위해 df 가공함
df_pure['Buy'] = np.nan
for i in Buy:
    df_all['Buy'].iloc[i] = df_all['Close'].iloc[i]

df_all['Sell'] = np.nan
for i in Sell:
    df_all['Sell'].iloc[i] = df_all['Close'].iloc[i]

# DataFrame 보기
with st.expander('데이터프레임 보기'):
    st.dataframe(df_pure)

with st.expander('Squeeze 데이터프레임 보기'):
    st.dataframe(df_squeeze)

# ------------------------ MPLFinance 시작

ohcl = df_squeeze[['Open', 'High', 'Close', 'Low']]

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
fig = plt.figure(figsize=(20, 10))

apds = [mpf.make_addplot(df_squeeze['value'], panel=1, type='bar', color=colors, alpha=0.8, secondary_y=False),
        mpf.make_addplot([0] * len(df_squeeze), panel=1, type='scatter', marker='x', markersize=50,
                         color=['gray' if s else 'black' for s in df_squeeze['squeeze_off']], secondary_y=False)]

mpf.plot(ohcl,
         volume_panel=2,
         figratio=(3, 1),
         figscale=4,
         style='charles',
         type='candle',
         addplot=apds,
         returnfig=True)

st.pyplot()



