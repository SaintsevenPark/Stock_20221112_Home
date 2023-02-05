import sys
import pandas as pd
import streamlit as st
import time
import datetime
import pyupbit

sys.path.append('/StockDashboard01/pages/saintsevenlib')
from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst

# -------------------- 페이지 형태 최기화
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# --------------------- 각종 변수 초기화
l_line = 2
s_line = -10
default_strategy = 11
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
    "Strategy 12": sst.strategy12,
}

df_coinlist = pyupbit.get_tickers(fiat='KRW')
selected_strategy = st.sidebar.selectbox("전략 선택", strategy_names_to_funcs.keys(), index=default_strategy)


# ------------------------------------ Puypbit --------------------------------------------
buy_coin_num = []
buy_coin_symbol = []
buy_coin_name = []
buy_coin_price = []
#
with st.expander("코인 목록 확장"):
    st.dataframe(df_coinlist)
    st.selectbox("종목선택", df_coinlist)
    st.write(len(df_coinlist))

progress_bar = st.progress(0.0)
if st.button("업비트 에서 종목 검색"):
    numbers = st.sidebar.empty()
    info = st.empty()
    num_tick = 0

    for i in range(len(df_coinlist)-1):
        with numbers.container():
            df = pyupbit.get_ohlcv(ticker=df_coinlist[i], interval='minute60')
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Value']
            df = ssl.get_indicator(df, l_line, s_line)
            st.write(f"{df_coinlist[i]} :  {df['Close'].iloc[-1]}")
            # ***********************************************************************************
            Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_strategy](df)
            st.write(desc)
            # ***********************************************************************************
            if len(Buy) > 0:
                if Buy[-1] >= len(df)-2:
                    con_text = "매수"
                    buy_coin_num.append(i)
                    buy_coin_name.append(df_coinlist[i])
                    buy_coin_price.append(df['Close'].iloc[-1])
                else:
                    con_text = "매도"
            if len(superBuy) > 0:
                if superBuy[-1] >= len(df)-2:
                    con_text = "매수"
                    buy_coin_num.append(i)
                    buy_coin_name.append(df_coinlist[i])
                    buy_coin_price.append(df['Close'].iloc[-1])
                else:
                    con_text = "매도"
            rtn = f"({num_tick}). {df_coinlist[i]}"
            st.text(rtn)
        num_tick = num_tick + 1
        progress_bar.progress(int(100 * num_tick / len(df_coinlist)+1))
        time.sleep(1)

    with info.container():
        st.sidebar.text("완료")
    df_boughtCoin_file = pd.DataFrame()
    df_boughtCoin_file['Num'] = buy_coin_num
    df_boughtCoin_file['Name'] = buy_coin_name
    df_boughtCoin_file['Price'] = buy_coin_price
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M_%S')
    st.dataframe(df_boughtCoin_file)
    df_boughtCoin_file.to_csv(f".\\bought data\\Coin_{now}_{selected_strategy}.csv")
