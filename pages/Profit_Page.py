import sys
import pandas as pd
import pyupbit
import streamlit as st
import FinanceDataReader as fdr
import time

# # https://lumiamitie.github.io/python/cufflinks_basic/ Cufflinks 참조
# # import plotly.offline as plyo

sys.path.append('/StockDashboard01/pages/saintsevenlib')

start_date = '2022-11'


tab1, tab2, tab3 = st.tabs(['NASDAQ', 'KRX', 'UPBIT'])

with tab1:
    # ------------------------ Nasdaq
    upload_file = st.file_uploader("NASDAQ CSV 선택")
    st.text(upload_file)

    if upload_file:
        df = pd.read_csv(upload_file)
        df.drop(df.columns[0], axis=1, inplace=True)

        # Current price 확인
        current_price = []
        for i in range(len(df)):
            df_current = fdr.DataReader(df['Symbol'].iloc[i], start_date)
            current_price.append(df_current['Close'].iloc[-1])
            time.sleep(0.3)

        df['현재가'] = current_price
        df['차액'] = df['현재가'] - df['Price']
        df['수익률'] = (df['차액'] / df['Price']) * 100

        st.dataframe(df)


with tab2:
    # ------------------------ KRX
    upload_file = st.file_uploader("KRX CSV 선택")
    st.text(upload_file)

    if upload_file:
        df = pd.read_csv(upload_file)
        df.drop(df.columns[0], axis=1, inplace=True)

        # Current price 확인
        current_price = []
        for i in range(len(df)):
            df_current = fdr.DataReader(str(df['Code'].iloc[i]).zfill(6), start_date)
            current_price.append(df_current['Close'].iloc[-1])
            time.sleep(0.3)

        df['현재가'] = current_price
        df['차액'] = df['현재가'] - df['Price']
        df['수익률'] = (df['차액'] / df['Price']) * 100

        st.dataframe(df)


with tab3:
    # ------------------------ UPBIT
    upload_file = st.file_uploader("배수 코인 CSV 선택")
    st.text(upload_file)

    if upload_file:
        df = pd.read_csv(upload_file)
        df.drop(df.columns[0], axis=1, inplace=True)

        # Current price 확인
        current_price = []
        for i in range(len(df)):
            df_current = pyupbit.get_current_price(ticker=df['Name'].iloc[i])
            current_price.append(df_current)
            time.sleep(0.3)

        df['현재가'] = current_price
        df['차액'] = df['현재가'] - df['Price']
        df['수익률'] = (df['차액'] / df['Price']) * 100

        st.dataframe(df)
