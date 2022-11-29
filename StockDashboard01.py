import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
# import matplotlib.pyplot as plt
# import time
# import numpy as np
# import cufflinks as cf
# # # https://lumiamitie.github.io/python/cufflinks_basic/ Cufflinks 참조
# import plotly.offline as plyo
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import pandas_ta as pt
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from plotly.subplots import make_subplots
#
from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst


# -------------------- 페이지 형태 최기화
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.markdown("https://medium.com/codex/step-by-step-implementation-of-the-supertrend-indicator-in-python-656aa678c111")
st.markdown("https://www.youtube.com/watch?v=u1b5v2Is8iY")

# st.markdown("### 테스트 페이지")
# 변수초기화
stock_count = 100

df_stocklist = pd.DataFrame()
# 새로 읽어올때만 실행
# df = fdr.StockListing('KRX')
# df.to_csv('stocklist_krx.csv')
df = pd.read_csv('stocklist_krx.csv')

df_stocklist['index'] = df[0:stock_count].index
df_stocklist['Code'] = df[0:stock_count]['Code']
df_stocklist['Name'] = df[0:stock_count]['Name']
st.sidebar.dataframe(df_stocklist)

number = st.number_input('Insert a number', min_value=0, max_value=stock_count)

tick_code = df_stocklist['Code'].iloc[number]
df = fdr.DataReader(tick_code, '2022')
df = ssl.get_indicator(df)

# st.dataframe(df)

#   작전 선택
l_line = 2
s_line = -10
Buy, Sell, superBuy, superSell, desc = sst.strategy09(df, l_line=l_line, s_line=s_line)
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### {df_stocklist['Name'].iloc[number]}  | 현재가 : {df['Close'].iloc[-1]}")
with col2:
    st.write(desc)

# 시각화 시작
df['SUPERTl2'] = df['SUPERTl'] * (1 + (l_line / 100))
df['SUPERTs2'] = df['SUPERTs'] * (1 + (s_line / 100))
fig = df[['Close', 'SUPERTl', 'SUPERTl2', 'SUPERTs', 'SUPERTs2']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="Super Trend")
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)

fig = df[['STOCHRSIk', 'STOCHRSId']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="Stochastic RSI")
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)

fig = df['SUPERTp'].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="Super Trend의 편차")
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))

fig.add_hline(y=s_line, line=dict(width=1, color='green', dash='dash'))
fig.add_hline(y=l_line, line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(fig)

