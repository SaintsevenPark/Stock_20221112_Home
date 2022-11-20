import sys
import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
import cufflinks as cf
# # https://lumiamitie.github.io/python/cufflinks_basic/ Cufflinks 참조
# # import plotly.offline as plyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as pt
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

sys.path.append('E:/MyProject/PyCharm_Project/StockProject01/StockDashboard01/saintsevenlib')
from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst


# -------------------- 페이지 형태 최기화
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# --------------------- 각종 변수 초기화
stock_length = 100
start_date = '2022'
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


df_stocklist = pd.read_csv('stocklist_nasdaq.csv')[0:stock_length]
df_stocklist.drop([df_stocklist.columns[0], df_stocklist.columns[3], df_stocklist.columns[4]], axis=1, inplace=True)

with st.sidebar.expander("종목목록 확장"):
    st.dataframe(df_stocklist)
    st.selectbox("종목선택", df_stocklist)
    st.write(len(df_stocklist))

selected_strategy = st.sidebar.selectbox("전략 선택", strategy_names_to_funcs.keys(), index=default_strategy)

buy_stock_symbol = []
buy_stock_name = []
buy_stock_price = []
progress_bar = st.sidebar.progress(0.0)
# -------------------- 종목 검색
if st.sidebar.button("코인 검색"):
    numbers = st.sidebar.empty()
    info = st.empty()
    num_tick = 0

    for i in range(len(df_stocklist)-1):
        with numbers.container():
            df = fdr.DataReader(df_stocklist['Symbol'].iloc[i], start_date)
            df = ssl.get_indicator(df)
            # ***********************************************************************
            Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_strategy](df)
            st.write(desc)
            # ***********************************************************************
            if len(Buy) > 0:
                # if Buy[-1] >= 198:
                if Buy[-1] >= len(df)-2:
                    con_text = "매수"
                    buy_stock_symbol.append(df_stocklist['Symbol'].iloc[i])
                    buy_stock_name.append(df_stocklist['Name'].iloc[i])
                    buy_stock_price.append(df['Close'].iloc[-1])
                else:
                    con_text = "매도"
            if len(superBuy) > 0:
                # if superBuy[-1] >= 198:
                if superBuy[-1] >= len(df)-2:
                    con_text = "매수"
                    buy_stock_symbol.append(df_stocklist['Symbol'].iloc[i])
                    buy_stock_name.append(df_stocklist['Name'].iloc[i])
                    buy_stock_price.append(df['Close'].iloc[-1])
                else:
                    con_text = "매도"
            rtn = f"({num_tick}). {df_stocklist['Symbol'].iloc[i]}-{df_stocklist['Name'].iloc[i]}"
            st.text(rtn)
        num_tick = num_tick + 1
        progress_bar.progress(int(100 * num_tick / len(df_stocklist)+1))
        time.sleep(0.5)

    with info.container():
        st.sidebar.text("완료")
    df_boughtStock_file = pd.DataFrame()
    df_boughtStock_file['Symbol'] = buy_stock_symbol
    df_boughtStock_file['Name'] = buy_stock_name
    df_boughtStock_file['Price'] = buy_stock_price
    df_boughtStock_file.to_csv(f".\\bought data\\bought_stock_nasdaq_{datetime.date.today()}_{selected_strategy}.csv")
    st.write(datetime.datetime.now())

