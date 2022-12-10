import pandas as pd
import configparser
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
# import time
import numpy as np
import cufflinks as cf
# # # https://lumiamitie.github.io/python/cufflinks_basic/ Cufflinks 참조
# import plotly.offline as plyo
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import pandas_ta as pt
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from plotly.subplots import make_subplots
import pandas_ta as pt
#
from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst


# --------------------- 설정 파일 작성
# config = configparser.ConfigParser()
# config['DefaultStrategy'] = {}                # 섹션을 생성한다
# config['DefaultStrategy']['DefaultStrategy'] = '8'      # 섹션 아래 실제 값을 생성한다
# with open('.\\config data\\config.ini', 'w') as configfile:
#     config.write(configfile)

# -------------------- 페이지 형태 최기화
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# ---------------------  초기화 변수
default_strategy = 8
l_line = 2
s_line = -10
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


def get_stock_list():
    df = fdr.StockListing('KRX')
    df.to_csv('stocklist_krx.csv')


def plot_by_plotly():
    # 지수 불러오기
    indices = ['KS11', 'KQ11', 'DJI', 'IXIC']
    col1, col2 = st.columns(2)
    with col1:
        select_indices = st.selectbox('지수', indices)
    with col2:
        selected_stratege = st.selectbox("전략 선택", strategy_names_to_funcs.keys(), index=default_strategy)

    df_indices = fdr.DataReader(select_indices, '2022')
    df_indices = ssl.get_indicator(df_indices)
    with st.expander('데이터 프레임'):
        st.dataframe(df_indices)

    if selected_stratege == 'Strategy 9' or selected_stratege == 'Strategy 10' or selected_stratege == 'Strategy 11':
        Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_stratege](df_indices, l_line, s_line)
        st.write(desc)
    else:
        Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_stratege](df_indices)
        st.write(desc)

    fig = df_indices[['Close', 'SUPERTl', 'SUPERTs']].iplot(asFigure=True, xTitle="The X Axis",
                                                            yTitle="The Y Axis", title="일간 가격 변동")
    st.plotly_chart(fig)

    fig = df_indices[['STOCHRSIk', 'STOCHRSId']].iplot(asFigure=True, xTitle="The X Axis",
                                                       yTitle="The Y Axis", title="일간 가격 변동")
    st.plotly_chart(fig)

def plot_by_matplotlib():
    # 지수 불러오기
    indices = ['KS11', 'KQ11', 'DJI', 'IXIC']
    col1, col2 = st.columns(2)
    with col1:
        select_indices = st.selectbox('지수', indices)
    with col2:
        selected_stratege = st.selectbox("전략 선택", strategy_names_to_funcs.keys(), index=default_strategy)

    df_indices = fdr.DataReader(select_indices, '2022')
    df_indices = ssl.get_indicator(df_indices, l_line, s_line)
    with st.expander('데이터 프레임'):
        st.dataframe(df_indices)

    Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_stratege](df_indices)
    st.write(desc)

    # MatPlotlib에서 마킹하기 위해 df 가공함
    df_indices['Buy'] = np.nan
    for i in Buy:
        df_indices['Buy'].iloc[i] = df_indices['Close'].iloc[i]

    df_indices['Sell'] = np.nan
    for i in Sell:
        df_indices['Buy'].iloc[i] = df_indices['Close'].iloc[i]

    # ---------------------------- Matplotlib 시작
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.style.use('fivethirtyeight')
    fig = plt.figure(figsize=(30, 25))
    ax1 = plt.subplot(4, 1, 1)
    plt.plot(df_indices['Close'], linewidth=1, label='CLOSING PRICE')
    plt.plot(df_indices['SUPERTl'], linewidth=0.5, label='SUPER TRENDl')
    # plt.plot(df['SUPERTlp'], linewidth = 1, label = 'SUPER TRENDl %')
    plt.plot(df_indices['SUPERTs'], linewidth=0.5, label='SUPER TRENDs')
    # plt.plot(df['SUPERTsp'], linewidth = 1, label = 'SUPER TRENDs %')
    # plt.plot(df['EMA200'], linewidth = 1, label = 'EMA200')
    plt.plot(df_indices.index, df_indices['Buy'], marker='^', color='r', markersize=10, linewidth=0, label='BUY SIGNAL')
    # plt.plot(df.index, df['Sell'], marker='v', color='green', markersize=10, linewidth=0, label='Sell SIGNAL')

    plt.fill_between(df_indices.index, df_indices['SUPERTl'], df_indices['SUPERTlp'], color='r', alpha=0.1)
    plt.fill_between(df_indices.index, df_indices['SUPERTs'], df_indices['SUPERTsp'], color='b', alpha=0.1)
    plt.title("Super Trend")
    plt.legend(loc='best')
    # plt.axis('off')

    ax2 = plt.subplot(4, 1, 2, sharex=ax1)
    plt.plot(df_indices['STOCHRSIk'], linewidth=1, label='STOCHRSIk')
    plt.plot(df_indices['STOCHRSId'], linewidth=1, label='STOCHRSId')
    plt.plot(df_indices.index, (df_indices['Buy'] * 0) + df_indices['STOCHRSIk'], marker='^', color='r', markersize=10, linewidth=0,
             label='BUY SIGNAL')
    plt.axhline(y=20, color='red', linewidth=0.8, linestyle='--')
    plt.title('Stochastic RSI')
    plt.legend(loc='best')
    plt.subplots_adjust(wspace=.025, hspace=0.2)

    ax3 = plt.subplot(4, 1, 3, sharex=ax1)
    plt.plot(df_indices['Close'], linewidth=1, label='CLOSE')
    plt.plot(df_indices['SMA5'], linewidth=1, label='SMA 5')
    plt.plot(df_indices['SMA20'], linewidth=1, label='SMA 20')
    plt.plot(df_indices.index, df_indices['Buy'], marker='^', color='r', markersize=10, linewidth=0, label='BUY SIGNAL')
    plt.title('SMA 5-20 X')
    plt.legend(loc='best')
    plt.subplots_adjust(wspace=.025, hspace=0.2)

    ax4 = plt.subplot(4, 1, 4, sharex=ax1)
    plt.plot(df_indices['Close'], linewidth=1, label='CLOSE')
    # plt.plot(df['BBL'], linewidth = 0.5, label = 'BBL', linestyle='--')
    # plt.plot(df['BBM'], linewidth = 0.5, label = 'BBM')
    plt.fill_between(df_indices.index, df_indices['BBL'], df_indices['BBM'], color='r', alpha=0.1)
    # plt.plot(df['BBU'], linewidth = 0.5, label = 'BBU')
    plt.fill_between(df_indices.index, df_indices['BBU'], df_indices['BBM'], color='green', alpha=0.1)
    plt.plot(df_indices.index, df_indices['Buy'], marker='^', color='r', markersize=10, linewidth=0, label='BUY SIGNAL')
    plt.title('Bollinger Band')
    plt.legend(loc='best')
    plt.subplots_adjust(wspace=.025, hspace=0.2)

    st.pyplot()


if __name__ == '__main__':
    # get_stock_list()
    # plot_by_plotly()
    plot_by_matplotlib()