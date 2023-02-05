import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np

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
df = fdr.DataReader(tick_code, '2022')
df = ssl.get_indicator(df, l_line, s_line)
stock_code = df_stocklist['Code'].iloc[number]
stock_name = df_stocklist['Name'].iloc[number]
stock_price = df['Close'].iloc[-1]
# Heiken Ashi
df_heiken = ssl.heikin_ashi(df)

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

# DataFrame 보기
with st.expander('데이터프레임 보기'):
    st.dataframe(df)

with st.expander('하이켄 아시 데이터프레임 보기'):
    st.dataframe(df_heiken)

# ------------------------ Plotly 시작
# Close
# fig = df_heiken.iplot(type='candle', asFigure=True, xTitle="The X Axis", yTitle="The Y Axis", title="일간 가격 변동")
# for i in range(len(Buy)):
#     fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
# for i in range(len(Sell)):
#     fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
# st.plotly_chart(fig)

# ------------------------ MPLFinance 시작

ohcl = df_heiken[['Open', 'High', 'Close', 'Low']]
ohcl = ohcl.astype(int)

st.set_option('deprecation.showPyplotGlobalUse', False)
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(30, 10))

mpf.plot(ohcl,
         volume_panel=2,
         figratio=(4, 1),
         figscale=4,
         style='charles',
         type='candle',
         returnfig=True)

st.pyplot()





