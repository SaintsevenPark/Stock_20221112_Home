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


# -------------------- 페이지 형태 최기화
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)


df_stocklist_100 = pd.DataFrame()
# 새로 잃어올때만 실행
# df = fdr.StockListing('NASDAQ')
# df.to_csv('stocklist_nasdaq.csv')
df = pd.read_csv('stocklist_nasdaq.csv')

df_stocklist_100['index'] = df[0:200].index
df_stocklist_100['Symbol'] = df[0:200]['Symbol']
df_stocklist_100['Name'] = df[0:200]['Name']
# st.dataframe(df)


st.sidebar.markdown("## NASDAQ")
col1, col2 = st.sidebar.columns([9, 1])
with col1:
    # ------------------- 매수 종목  리스트 AgGrid
    gd = GridOptionsBuilder.from_dataframe(df_stocklist_100)
    gd.configure_selection(selection_mode='sel_mode', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(df_stocklist_100,
                        gridOptions=gridoptions,
                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                        allow_unsafe_jscode=True)
    sel_row = grid_table["selected_rows"]
    # stock_index = sel_row[0]['StockIndex']        # 필요 없지만 예비로 남겨줌
    tick_code = sel_row[0]['Symbol']
    tick_name = sel_row[0]['Name']
    selected_stock = f"{tick_code} -- {tick_name}"
st.markdown(f"### {selected_stock}")
# -------------------------------------------------

df = fdr.DataReader(tick_code, '2022')
df = ssl.get_indicator(df)
# st.dataframe(df.tail(10))

# ====================   전략 선택 매수 마킹 ===========================
# 5 이평선이 20 이평선 아래에서 V 자 반등 할고 rsi가 우상 mfi가 우상
# Buy, Sell, superBuy, superSell = sst.strategy01(df)
# 5 이평선이 20 이평선을 돌파 할때
Buy, Sell, superBuy, superSell = sst.strategy03(df)


# ----------------------------------
fig = df[['Close', 'BBL', 'BBU', 'SMA5', 'SMA20']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="일간 가격 변동")
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=2, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=2, color='blue', dash='dash'))
st.plotly_chart(fig)
# 이동평균선
fig = df[['Close', 'SMA5', 'SMA20']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="이동평균선 5와 20 교차")
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=2, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=2, color='blue', dash='dash'))
st.plotly_chart(fig)
# Super Trend
fig = df[['Close', 'SUPERTl', 'SUPERTs']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="Super Trend")
for i in range(len(superBuy)):
    fig.add_vline(x=df.iloc[superBuy].index[i], line=dict(width=2, color='red', dash='dash'))
for i in range(len(superSell)):
    fig.add_vline(x=df.iloc[superSell].index[i], line=dict(width=2, color='blue', dash='dash'))
st.plotly_chart(fig)
# 볼린저밴드
fig = df[['Close', 'BBL', 'BBU']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="볼린저 밴드")
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=2, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=2, color='blue', dash='dash'))
st.plotly_chart(fig)
# RSI
fig = df['RSI'].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="RSI")
fig.add_hline(y=30, line=dict(width=1, color='pink', dash='dash'))
fig.add_hline(y=70, line=dict(width=1, color='cyan', dash='dash'))
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=2, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=2, color='blue', dash='dash'))
st.plotly_chart(fig)
# MFI
fig = df['MFI'].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="MFI")
fig.add_hline(y=30, line=dict(width=1, color='pink', dash='dash'))
fig.add_hline(y=70, line=dict(width=1, color='cyan', dash='dash'))
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=2, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=2, color='blue', dash='dash'))
st.plotly_chart(fig)
# MACD
fig = df[['MACD', 'MACDs']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="MACD")
fig.add_hline(y=0, line=dict(width=1, color='pink', dash='dash'))
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=2, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=2, color='blue', dash='dash'))
st.plotly_chart(fig)
# CCI
fig = df['CCI'].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="CCI")
fig.add_hline(y=100, line=dict(width=1, color='pink', dash='dash'))
fig.add_hline(y=-100, line=dict(width=1, color='cyan', dash='dash'))
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=2, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=2, color='blue', dash='dash'))
st.plotly_chart(fig)


