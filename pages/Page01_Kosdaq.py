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
#
from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst


# -------------------- 페이지 형태 최기화
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

default_strategy = 0
strategy_names_to_funcs = {
    "Strategy 1": sst.strategy01,
    "Strategy 2": sst.strategy02,
    "Strategy 3": sst.strategy03,
    "Strategy 4": sst.strategy04,
    "Strategy 5": sst.strategy05,
    "Strategy 6": sst.strategy06,
    "Strategy 7": sst.strategy07,
    "Strategy 8": sst.strategy08,
}

df_stocklist_100 = pd.DataFrame()
# 새로 읽어올때만 실행
# df = fdr.StockListing('KRX')
# df.to_csv('stocklist_krx.csv')
df = pd.read_csv('stocklist_krx.csv')

df_stocklist_100['index'] = df[0:200].index
df_stocklist_100['Code'] = df[0:200]['Code']
df_stocklist_100['Name'] = df[0:200]['Name']
# st.dataframe(df)

st.sidebar.markdown("## KOSPI")
selected_strategy = st.sidebar.selectbox("전략 선택", strategy_names_to_funcs.keys(), index=default_strategy)
col1, col2 = st.sidebar.columns([9, 1])
with col1:
    # ------------------- 매수 종목  리스트 AgGrid
    gd = GridOptionsBuilder.from_dataframe(df_stocklist_100)
    gd.configure_selection(selection_mode='sel_mode', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(df_stocklist_100,
                        gridOptions=gridoptions,
                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                        allow_unsafe_jscode=True,
                        columns_auto_size_mode=True,
                        columeSize='sizeFit',
                        )
    sel_row = grid_table["selected_rows"]
    # stock_index = sel_row[0]['StockIndex']        # 필요 없지만 예비로 남겨줌
    tick_code = sel_row[0]['Code']
    tick_name = sel_row[0]['Name']
    selected_stock = f"[{tick_code}] {tick_name}"
st.markdown(f"### {selected_stock}")
# -------------------------------------------------

df = fdr.DataReader(tick_code, '2022')
df = ssl.get_indicator(df)
st.write(df['Close'].iloc[-1])
# st.dataframe(df.tail(10))

# ====================   전략 선택 매수 마킹 ===========================
# st.write('5 이평선이 20 이평선 아래에서 V 자 반등 할고 rsi가 우상 mfi가 우상')
Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_strategy](df)
st.write(desc)

# 5 이평선이 20 이평선을 돌파 할때
# Buy, Sell, superBuy, superSell = sst.strategy03(df)
# st.write('전략3 : 5 이평선이 20 이평선을 돌파 할때')

# # TRIX 가 0을 돌파할때
# Buy, Sell, superBuy, superSell = sst.strategy07(df)
# st.write('TRIX 가 0을 돌파할때')

# TRIX 가 TRIXs 를 돌파할때
# Buy, Sell, superBuy, superSell = sst.strategy08(df)
# st.write('TRIX 가 TRIXs 를 돌파할때')


# ----------------------------------
fig = df[['Close', 'BBL', 'BBU', 'SMA5', 'SMA20']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="일간 가격 변동")
for i in range(len(Buy)):
    fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
for i in range(len(Sell)):
    fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
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
                        yTitle="The Y Axis", title="Super Trend", theme='space')
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
fig.add_hline(y=30, line=dict(width=2, color='pink', dash='dash'))
fig.add_hline(y=70, line=dict(width=2, color='cyan', dash='dash'))
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




