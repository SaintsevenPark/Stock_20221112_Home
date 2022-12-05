import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import time
import numpy as np
import pandas as pd
import plotly.offline as plyo
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

#
from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst


# -------------------- 페이지 형태 최기화
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# 변수초기화
stock_count = 100
df_stocklist_krx = pd.DataFrame()
df_stocklist_nasdaq = pd.DataFrame()

df_krx = pd.read_csv('stocklist_krx.csv')
df_stocklist_krx['index'] = df_krx[0:stock_count].index
df_stocklist_krx['Code'] = df_krx[0:stock_count]['Code']
df_stocklist_krx['Name'] = df_krx[0:stock_count]['Name']

df_nasdaq = pd.read_csv('stocklist_nasdaq.csv')
df_stocklist_nasdaq['index'] = df_nasdaq[0:stock_count].index
df_stocklist_nasdaq['Symbol'] = df_nasdaq[0:stock_count]['Symbol']
df_stocklist_nasdaq['Name'] = df_nasdaq[0:stock_count]['Name']

with st.sidebar.expander("코스닥 항목 보기"):
    st.dataframe(df_stocklist_krx)

with st.sidebar.expander("나스닥 항목 보기"):
    st.dataframe(df_stocklist_nasdaq)

# --------------------------- Tab
tab1, tab2 = st.tabs(["KOSDAQ", "NASDAQ"])

with tab1:
    number = st.number_input('Insert a number', min_value=0, max_value=stock_count)

    tick_code = df_stocklist_krx['Code'].iloc[number]
    df = fdr.DataReader(tick_code, '2022')
    df = ssl.get_indicator(df)

    with st.expander("종목 데이터 보기"):
        st.dataframe(df)

    stock_name = df_stocklist_krx['Name'].iloc[number]
    stock_code = df_stocklist_krx['Code'].iloc[number]
    stock_price = df['Close'].iloc[-1]
    st.markdown(f"### [{stock_code}] {stock_name} : {stock_price}")

    #   작전 선택
    l_line = 2
    s_line = -10
    # Buy, Sell, superBuy, superSell, desc = sst.strategy09(df, l_line=l_line, s_line=s_line)
    Buy, Sell, superBuy, superSell, desc = sst.strategy10(df, l_line=l_line, s_line=s_line)

    # -----------------------------Plotly Start ----------------
    fig = make_subplots(
        rows=6, cols=1,
        # start_cell="bottom-left",  # 시작 위치를 바꿀 수 있음
        shared_xaxes= True,
        # horizontal_spacing=0.01,
        vertical_spacing=0.01,
        subplot_titles=("종가-SuperTrend", "%SuperTrend", "StochasticRSI", "단순이동 평균") # 각 Subplot 별 subtitle 넣기
    )

    fig.add_trace(go.Line(x=df.index, y=df['Close'], line_width=1, name='Close',
                          legendgroup ='1',
                          ),
                  row=1, col=1)
    fig.add_trace(go.Line(x=df.index, y=df['SUPERTl'], line_width=2, name='SUPERl',
                          legendgroup ='1',
                          # fill='tonexty',
                          ),
                  row=1, col=1)
    fig.add_trace(go.Line(x=df.index, y=df['SUPERTl'] * (1 + (l_line / 100)), line_width=0.5, name='SUPERl %',
                          legendgroup='1',
                          ),
                  row=1, col=1)

    fig.add_trace(go.Line(x=df.index, y=df['SUPERTs'], line_width=2, name='SUPERs',
                          legendgroup ='1',
                          ),
                  row=1, col=1)
    fig.add_trace(go.Line(x=df.index, y=df['SUPERTs'] * (1 + (s_line / 100)), line_width=0.5, name='SUPERTs %',
                          legendgroup='1',
                          ),
                  row=1, col=1)

    # SUPERTREND %
    fig.add_trace(go.Line(x=df.index, y=df['SUPERTp'], line_width=1, name='SUPER %',
                          legendgroup ='2',
                          ),
                  row=2, col=1)

    # Stockastic RSI
    fig.add_trace(go.Line(x=df.index, y=df['STOCHRSIk'], line_width=1, name='STOCKRSIk',
                          legendgroup='3',
                          ),
                  row=3, col=1)
    fig.add_trace(go.Line(x=df.index, y=df['STOCHRSId'], line_width=1, name='STOCKRSId',
                          legendgroup='3',
                          ),
                  row=3, col=1)

    # 단순이동 평균선 5 - 20
    fig.add_trace(go.Line(x=df.index, y=df['SMA5'], line_width=2, name='SMA5',
                          legendgroup ='4'), row=4, col=1)
    fig.add_trace(go.Line(x=df.index, y=df['SMA20'], line_width=1, name='SMA20',
                          legendgroup ='4'), row=4, col=1)

    # RSI
    fig.add_trace(go.Line(x=df.index, y=df['RSI'], line_width=2, name='RSI',
                          legendgroup='5'), row=5, col=1)

    # MFI
    fig.add_trace(go.Line(x=df.index, y=df['MFI'], line_width=2, name='MFI',
                          legendgroup='6'), row=6, col=1)

    # ---------------------- 마킹
    for i in range(len(Buy)):
        fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='orange', dash='dash'))
    for i in range(len(Sell)):
        fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))

    fig.add_hline(y=l_line, line_width=1, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=s_line, line_width=1, line_dash="dash", line_color="green", row=2, col=1)

    fig.add_hline(y=20, line_width=1, line_dash="dash", line_color="green", row=3, col=1)

    fig.add_hline(y=30, line_width=1, line_dash="dash", line_color="purple", row=4, col=1)
    fig.add_hline(y=70, line_width=1, line_dash="dash", line_color="purple", row=4, col=1)

    fig.add_hline(y=30, line_width=1, line_dash="dash", line_color="purple", row=5, col=1)
    fig.add_hline(y=50, line_width=1, line_dash="dash", line_color="purple", row=5, col=1)
    fig.add_hline(y=70, line_width=1, line_dash="dash", line_color="purple", row=5, col=1)
    # fig.add_hline(y=15000, line_width=1, line_dash="dash", line_color="pink", row=1, col=1)
    fig.update_layout(height=2000, width=600,
                      legend_tracegroupgap = 130,)

    st.plotly_chart(fig, use_container_width = True)



with tab2:
    number = st.number_input('Insert a Nasdaq Code Index ', min_value=0, max_value=stock_count)

    tick_code = df_stocklist_nasdaq['Symbol'].iloc[number]
    df = fdr.DataReader(tick_code, '2022')
    df = ssl.get_indicator(df)
    df['SUPERTp'] = ((df['Close'] - df['SUPERT']) / df['Close']) * 100

    with st.expander("종목 데이터 보기"):
        st.dataframe(df)

    stock_name = df_stocklist_nasdaq['Name'].iloc[number]
    stock_code = df_stocklist_nasdaq['Symbol'].iloc[number]
    stock_price = df['Close'].iloc[-1]
    st.markdown(f"### [{stock_code}] {stock_name} : {stock_price}")

    #   작전 선택
    l_line = 2
    s_line = -10
    Buy, Sell, superBuy, superSell, desc = sst.strategy09(df, l_line=l_line, s_line=s_line)

    # -----------------------------Plotly Start ----------------
    fig = make_subplots(
        rows=5, cols=1,
        # start_cell="bottom-left",  # 시작 위치를 바꿀 수 있음
        shared_xaxes= True,
        # horizontal_spacing=0.01,
        vertical_spacing=0.02,
        subplot_titles=("종가-SuperTrend", "%SuperTrend", "단순이동 평균") # 각 Subplot 별 subtitle 넣기
    )

    fig.add_trace(go.Line(x=df.index, y=df['Close'], line_width=1, name='Close',
                          legendgroup ='1',
                          # fill='toself',
                          ),
                  row=1, col=1)
    fig.add_trace(go.Line(x=df.index, y=df['SUPERTl'], line_width=2, name='SUPERl',
                          legendgroup ='1',
                          # fill='tonexty',
                          ),
                  row=1, col=1)
    fig.add_trace(go.Line(x=df.index, y=df['SUPERTl'] * (1 + (l_line / 100)), line_width=0.5, name='SUPERl_2',
                          legendgroup='1',
                          ),
                  row=1, col=1)

    fig.add_trace(go.Line(x=df.index, y=df['SUPERTs'], line_width=2, name='SUPERs',
                          legendgroup ='1',
                          # fill='tonexty',
                          ),
                  row=1, col=1)
    fig.add_trace(go.Line(x=df.index, y=df['SUPERTs'] * (1 + (s_line / 100)), line_width=0.5, name='SUPERs_2',
                          legendgroup='1',
                          ),
                  row=1, col=1)

    fig.add_trace(go.Line(x=df.index, y=df['SUPERTp'], line_width=1, name='SUPER %',
                          legendgroup ='2',
                          ),
                  row=2, col=1)

    # 이동 평균선
    fig.add_trace(go.Line(x=df.index, y=df['SMA5'], line_width=2, name='SMA5',
                          legendgroup ='3'), row=3, col=1)
    fig.add_trace(go.Line(x=df.index, y=df['SMA20'], line_width=1, name='SMA20',
                          legendgroup ='3'), row=3, col=1)

    # RSI
    fig.add_trace(go.Line(x=df.index, y=df['RSI'], line_width=2, name='RSI',
                          legendgroup='4'), row=4, col=1)

    # MFI
    fig.add_trace(go.Line(x=df.index, y=df['MFI'], line_width=2, name='MFI',
                          legendgroup='5'), row=5, col=1)

    # ---------------------- 마킹
    for i in range(len(Buy)):
        fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=3, color='pink', dash='dash'))
    for i in range(len(Sell)):
        fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=3, color='blue', dash='dash'))

    fig.add_hline(y=l_line, line_width=1, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=s_line, line_width=1, line_dash="dash", line_color="green", row=2, col=1)

    fig.add_hline(y=30, line_width=1, line_dash="dash", line_color="purple", row=4, col=1)
    fig.add_hline(y=70, line_width=1, line_dash="dash", line_color="purple", row=4, col=1)
    # fig.add_hline(y=15000, line_width=1, line_dash="dash", line_color="pink", row=1, col=1)
    fig.update_layout(height=2000, width=600,
                      legend_tracegroupgap = 135,)

    st.plotly_chart(fig, use_container_width = True)

