import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import time
import numpy as np
import pandas_ta as pt
import mplfinance as mpf

from plotly.subplots import make_subplots
import cufflinks as cf
import plotly.graph_objs as go

from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst


l_line = 2
s_line = -10
stock_count = 300
default_strategy = 8
start_year = '2022'

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
df_origin = fdr.DataReader(tick_code, start=start_year)
df_heiken = ssl.heikin_ashi(df_origin).astype(int)
df_squeeze = ssl.get_squeeze_momentum(df_origin)

# -----------------------------------------------------------------------
with st.expander("순수 데이터 프레임"):
    st.dataframe(df_origin)
with st.expander("Heiken Ashi 데이터 프레임"):
    st.dataframe(df_heiken)
with st.expander("Squeeze 데이터 프레임"):
    st.dataframe(df_squeeze)
df = ssl.get_indicator(df_origin, l_line, s_line)
with st.expander("모든 지표"):
    st.dataframe(df)
# -----------------------------------------------------------------------

stock_code = df_stocklist['Code'].iloc[number]
stock_name = df_stocklist['Name'].iloc[number]
stock_price = df['Close'].iloc[-1]

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


# -----------------------  Plotly 시작
# 1
trace1_1 = go.Scatter(x = df_origin.index,
                    y = df_origin['Close'],
                    name='종가'
                    )
trace1_2 = go.Scatter(x = df_origin.index,
                    y = df_origin['SUPERTl'],
                    name='슈퍼트렌드 l'
                    )
trace1_3 = go.Scatter(x = df_origin.index,
                    y = df_origin['SUPERTs'],
                    name='슈퍼트렌드 s'
                    )
trace1_4 = go.Scatter(x = df_origin.index,
                    y = df_origin['SUPERTlp'],
                    name='슈퍼트렌드 l %',
                    line=dict(width=0.5)
                    )
trace1_5 = go.Scatter(x = df_origin.index,
                    y = df_origin['SUPERTsp'],
                    name='슈퍼트렌드 s %',
                    line=dict(width=0.5)
                    )

# 2 - Stochastic
trace2_1 = go.Scatter(x=df_origin.index,
                    y=df_origin['STOCHRSIk'],
                    name='StochasticRSI K'
                    )
trace2_2 = go.Scatter(x=df_origin.index,
                    y=df_origin['STOCHRSId'],
                    name='StochasticRSI d'
                    )

# 3 - 5 , 20 이동평균선
trace3_1 = go.Scatter(x=df_origin.index,
                    y=df['SMA5'],
                    name='5일 이동평균선'
                    )
trace3_2 = go.Scatter(x=df_origin.index,
                    y=df['SMA20'],
                    name='20일 이동평균선'
                    )

# CandleStick
trace4_1 = go.Candlestick(x=df.index,
                          open=df_heiken['Open'],
                          high=df_heiken['High'],
                          low=df_heiken['Low'],
                          close=df_heiken['Close'],
                          name='Candle Stick'
                          )

data1 = [trace1_1, trace1_2, trace1_3, trace1_4, trace1_5]
data2 = [trace2_1, trace2_2]
data3 = [trace3_1, trace3_2]
data4 = [trace4_1]

fig1 = go.Figure(data=data1)
fig2 = go.Figure(data=data2)
fig3 = go.Figure(data=data3)
fig4 = go.Figure(data=data4)
fig4.update_layout(xaxis_rangeslider_visible=False)

figs = cf.subplots([fig1, fig2, fig3, fig4], shape=(4, 1))
figs['layout'].update(height=1600, title='PARTICLES CORRELATION')


# for i in range(len(Buy)):
#     fig.add_vline(x=df.iloc[Buy].index[i], line=dict(width=1, color='red', dash='dash'))
# for i in range(len(Sell)):
#     fig.add_vline(x=df.iloc[Sell].index[i], line=dict(width=1, color='blue', dash='dash'))
st.plotly_chart(figs, use_container_width=True)



