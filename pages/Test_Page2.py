import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
import matplotlib.pyplot as plt

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
    df['SUPERTl2'] = df['SUPERTl'] * (1 + (l_line / 100))
    df['SUPERTs2'] = df['SUPERTs'] * (1 + (s_line / 100))
    Buy, Sell, superBuy, superSell, desc = sst.strategy09(df, l_line=l_line, s_line=s_line)

    # -----------------------------Matplotlib Start ----------------
    # # plt.figure(figsize=(9, 7))
    # fig, ax = plt.subplots(2, 1)
    # ax[0] = df['Close'].plot(linewidth=0.5)
    # ax[1] = df['SUPERTl'].plot(linewidth=0.5)
    # # ax[0][1] = df['SUPERTs'].plot(linewidth=0.5)
    #
    #
    # st.pyplot(fig=fig, clear_figure=None)


    st.line_chart(df[['Close', 'SUPERTl', 'SUPERTs', 'SUPERTl2', 'SUPERTs2']])


