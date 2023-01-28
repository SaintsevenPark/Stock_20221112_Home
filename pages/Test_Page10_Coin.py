import pandas as pd
import streamlit as st
# from streamlit.components.v1 import html
import matplotlib.pyplot as plt
import time
import numpy as np
import pandas_ta as pt
import mplfinance as mpf
import pyupbit

from plotly.subplots import make_subplots
import cufflinks as cf
import plotly.graph_objs as go

from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst

# -------------------- 페이지 형태 최기화
st.set_page_config(page_title=None, page_icon="chart_with_upwards_trend", layout="wide", initial_sidebar_state="auto",
                   menu_items=None)

l_line = 2
s_line = -10
coin_list = pd.DataFrame(pyupbit.get_tickers('KRW'), columns=['CoinName'])
coin_count = len(coin_list) - 1
default_strategy = 8
interval = 1

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

list_interval = {
    "minute1",
    "minute3",
    "minute5",
    "minute10",
    "minute15",
    "minute30",
    "minute60",
    "minute240",
    "day",
    "week",
    "month",
}

# # &&&&&&&&& 떠다니는 버튼 테스트
# button = """
# <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="blackarysf" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" >
# </script>
# """
# html(button, height=70, width=220)
# st.markdown(
#     """
#     <style>
#         iframe[width="220"] {
#             position: fixed;
#             bottom: 60px;
#             right: 40px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
# # &&&&&&&&& 떠다니는 버튼 테스트 끝


selected_strategy = st.sidebar.selectbox("전략 선택", strategy_names_to_funcs.keys(), index=default_strategy)
selected_interval = st.sidebar.selectbox("인터벌 선택", list_interval, index=interval)
st.sidebar.write(selected_interval)

number = st.sidebar.number_input('Insert a number', min_value=0, max_value=coin_count)

coin_name = coin_list['CoinName'].iloc[number]

with st.sidebar.expander("코인 목록"):
    st.dataframe(coin_list)

# 주식종목 검색 텍스트박스
coin_name_search = st.sidebar.text_input('코인 검색', "코인명 입력")
coin_search_index = coin_list[coin_list['CoinName'].str.contains(coin_name_search, case=False)]
st.sidebar.write("코인인엑스 : ", coin_search_index)

# ---------------- 코인 기초데이터 불러오기 -----------------------------------
df_pure = pyupbit.get_ohlcv(coin_name, selected_interval)
df_pure.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Value']
# st.dataframe(df_pure)
df_all = ssl.get_indicator(df_pure, l_line, s_line)
# st.dataframe(df_all)

# ---------------- 현재가
current_price = df_pure['Close'].iloc[-1]
st.sidebar.markdown(f"### {coin_name} : {current_price:00,} KRW")
# ----------------------- 코인 데이터 기공 -----------------------------------
df_heiken = ssl.heikin_ashi(df_pure).astype(int)
df_squeeze = ssl.get_squeeze_momentum(df_pure)
# st.dataframe(df_heiken)
# st.dataframe(df_squeeze)

# ====================   전략 선택 매수 마킹 ===========================
Buy, Sell, superBuy, superSell, desc = strategy_names_to_funcs[selected_strategy](df_all)
st.write(desc)

# MatPlotlib에서 마킹하기 위해 df 가공함
df_all['Buy'] = np.nan
for i in Buy:
    df_all['Buy'].iloc[i] = df_all['Close'].iloc[i]

df_all['Sell'] = np.nan
for i in Sell:
    df_all['Sell'].iloc[i] = df_all['Close'].iloc[i]

# =================== 필요한 정보만 정리해서 DataFrame 을 만듦
df_just = pd.DataFrame()
df_just['Open'] = df_all['Open']
df_just['High'] = df_all['High']
df_just['Low'] = df_all['Low']
df_just['Close'] = df_all['Close']
df_just['BBL'] = df_all['BBL']
df_just['BBM'] = df_all['BBM']
df_just['BBU'] = df_all['BBU']
df_just['Open_HI'] = df_heiken['Open']
df_just['High_HI'] = df_heiken['High']
df_just['Low_HI'] = df_heiken['Low']
df_just['Close_HI'] = df_heiken['Close']
df_just['SUPERTl'] = df_all['SUPERTl']
df_just['SUPERTs'] = df_all['SUPERTs']
df_just['SUPERTlp'] = df_all['SUPERTlp']
df_just['SUPERTsp'] = df_all['SUPERTsp']
df_just['STOCHRSIk'] = df_all['STOCHRSIk']
df_just['STOCHRSId'] = df_all['STOCHRSId']
df_just['SMA5'] = df_all['SMA5']
df_just['SMA20'] = df_all['SMA20']
df_just['SQ_value'] = df_all['value']
df_just['squeeze_off'] = df_all['squeeze_off']
df_just['squeeze_on'] = df_all['squeeze_on']
df_just['EMA200'] = df_all['EMA200']

df_just['Buy'] = df_all['Buy']
df_just['Sell'] = df_all['Sell']
with st.expander("필요한 지표만"):
    st.dataframe(df_just)

# *****************************************************************************
# ================================  시각화 시작 =================================
# *****************************************************************************
st.markdown(f"### {coin_name} : {current_price:00,} KRW")

# 1
trace1_1 = go.Scatter(x=df_just.index,
                      y=df_just['Close'],
                      name='종가',
                      legendgroup='종가',
                      legendrank=1,
                      )
trace1_2 = go.Scatter(x=df_just.index,
                      y=df_just['SUPERTl'],
                      name='슈퍼트렌드 l',
                      legendgroup='종가',
                      legendrank=1,
                      )
trace1_3 = go.Scatter(x=df_pure.index,
                      y=df_just['SUPERTs'],
                      name='슈퍼트렌드 s',
                      legendgroup='종가',
                      legendrank=1,
                      )
trace1_4 = go.Scatter(x=df_just.index,
                      y=df_just['SUPERTlp'],
                      name='슈퍼트렌드 l %',
                      legendgroup='종가',
                      legendrank=1,
                      line=dict(width=0.5)
                      )
trace1_5 = go.Scatter(x=df_just.index,
                      y=df_just['SUPERTsp'],
                      name='슈퍼트렌드 s %',
                      legendgroup='종가',
                      legendrank=1,
                      line=dict(width=0.5)
                      )
trace1_6 = go.Scatter(x=df_just.index,
                      y=df_just['Buy'],
                      name='Buy',
                      legendgroup='종가',
                      legendrank=1,
                      mode='markers',
                      marker=dict(
                          color='red',
                          size=10,
                          line=dict(
                              color='MediumPurple',
                              width=3
                          ))
                      )
trace1_7 = go.Scatter(x=df_just.index,
                      y=df_just['EMA200'],
                      name='EMA200',
                      legendgroup='종가',
                      legendrank=1,
                      )

# 2 - Stochastic
trace2_1 = go.Scatter(x=df_just.index,
                      y=df_just['STOCHRSIk'],
                      name='StochasticRSI K',
                      legendgroup='StochasticRSI K',
                      legendrank=2,
                      )
trace2_2 = go.Scatter(x=df_just.index,
                      y=df_just['STOCHRSId'],
                      name='StochasticRSI d',
                      legendgroup='StochasticRSI K'
                      )
trace2_3 = go.Scatter(x=df_just.index,
                      y=(df_just['Buy'] * 0) + df_just['STOCHRSId'],
                      name='Buy',
                      legendgroup='StochasticRSI K',
                      mode='markers',
                      marker=dict(
                          color='red',
                          size=10,
                          line=dict(
                              color='MediumPurple',
                              width=3
                          ))
                      )

# 3 - 5 , 20 이동평균선
trace3_1 = go.Scatter(x=df_just.index,
                      y=df_just['SMA5'],
                      name='5일 이동평균선',
                      legendgroup='5일 이동평균선',
                      legendrank=3
                      )
trace3_2 = go.Scatter(x=df_just.index,
                      y=df_just['SMA20'],
                      name='20일 이동평균선',
                      legendgroup='5일 이동평균선'
                      )
trace3_3 = go.Scatter(x=df_just.index,
                      y=df_just['Buy'] * 0.95,
                      name='Buy',
                      legendgroup='5일 이동평균선',
                      mode='markers',
                      marker=dict(
                          color='red',
                          size=10,
                          line=dict(
                              color='MediumPurple',
                              width=3
                          ))
                      )

# 4. Squeeze
colors = []

for ind, val in enumerate(df_just['SQ_value']):
    if val >= 0:
        color = 'green'
        if val > df_just['SQ_value'][ind - 1]:
            color = 'lime'
    else:
        color = 'maroon'
        if val < df_just['SQ_value'][ind - 1]:
            color = 'red'
    colors.append(color)

trace4_1 = go.Bar(x=df_just.index,
                      y=df_just['SQ_value'],
                      name='Squeeze',
                  marker=dict(color=colors),
                      legendgroup='Squeeze',
                      legendrank=4,
                      )
trace4_2 = go.Scatter(x=df_just.index,
                      y=(df_just['Buy'] * 0) + df_just['SQ_value'],
                      name='Buy',
                      legendgroup='Squeeze',
                      legendrank=4,
                      mode='markers',
                      marker=dict(
                          color='red',
                          # symbol="diamond",
                          size=10,
                          line=dict(
                              color='MediumPurple',
                              width=3
                          ))
                      )

trace4_3 = go.Scatter(x=df_just.index,
                      y=df_just['Close'] * 0,
                      name='Buy',
                      legendgroup='Squeeze',
                      legendrank=4,
                      mode='markers',
                      marker=dict(
                          color='yellow',
                          symbol="diamond",
                          size=3,
                          line=dict(
                              color=['blue' if s else 'red' for s in df_just['squeeze_off']],
                              width=2
                          ))
                      )
# color=['green' if s else 'red' for s in df_squeeze['squeeze_off']]


# 5. Heiken Ashi
trace5_1 = go.Candlestick(x=df_just.index,
                          open=df_just['Open_HI'],
                          high=df_just['High_HI'],
                          low=df_just['Low_HI'],
                          close=df_just['Close_HI'],
                          name='Heiken Ashi',
                          legendgroup='Heiken Ashi',
                          legendrank=5,
                          increasing_line_color='red',
                          decreasing_line_color='green',
                          )
trace5_2 = go.Scatter(x=df_just.index,
                      y=df_just['Buy'] * 1.05,
                      name='Buy',
                      legendgroup='Heiken Ashi',
                      legendrank=5,
                      mode='markers',
                      marker=dict(
                          color='red',
                          size=10,
                          line=dict(
                              color='MediumPurple',
                              width=3
                          ))
                      )



data1 = [trace1_1, trace1_2, trace1_3, trace1_4, trace1_5, trace1_6, trace1_7]
data2 = [trace2_1, trace2_2, trace2_3]
data3 = [trace3_1, trace3_2, trace3_3]
data4 = [trace4_1, trace4_2, trace4_3]
data5 = [trace5_1, trace5_2]

fig1 = go.Figure(data=data1)
fig2 = go.Figure(data=data2)
fig3 = go.Figure(data=data3)
fig4 = go.Figure(data=data4)
fig5 = go.Figure(data=data5)

figs = cf.subplots([fig1, fig2, fig3, fig4, fig5], shape=(5, 1))
# figs = cf.subplots([fig1, fig2, fig3], shape=(3, 1))
figs['layout'].update(height=1500, title='PARTICLES CORRELATION', legend_tracegroupgap = 180)
figs['layout'].update(xaxis5=dict(rangeslider=dict(visible=False)))
# figs['update_layout'](xaxis_rangeslider_visible=False, xaxis_rangeslider_visible=False)
# fig5.update(xaxis_rangeslider_visible=False)


st.plotly_chart(figs, use_container_width=True)

# -----------------------  HeikenAshi  Matplotlib 시작
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(30, 15))

mpf.plot(df_heiken,
         volume_panel=2,
         figratio=(5, 1),
         figscale=1,
         style='charles',
         type='candle',
         returnfig=True)

st.pyplot()

# -----------------------  Squeeze Momentum  Matplotlib 시작
ohcl_squeeze = df_squeeze[['Open', 'High', 'Close', 'Low']]

colors = []

for ind, val in enumerate(df_squeeze['value']):
    if val >= 0:
        color = 'green'
        if val > df_squeeze['value'][ind - 1]:
            color = 'lime'
    else:
        color = 'maroon'
        if val < df_squeeze['value'][ind - 1]:
            color = 'red'
    colors.append(color)

st.set_option('deprecation.showPyplotGlobalUse', False)
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(30, 15))

apds = [mpf.make_addplot(df_squeeze['value'], panel=1, type='bar', color=colors, alpha=0.5, secondary_y=False),
        mpf.make_addplot([0] * len(df_squeeze), panel=1, type='scatter', marker='x', markersize=80,
                         color=['green' if s else 'red' for s in df_squeeze['squeeze_off']], secondary_y=False),
        mpf.make_addplot(df_squeeze['EMA200'], panel=0, type='line', secondary_y=False),
        mpf.make_addplot(df_all['BBL'], panel=0, type='line', secondary_y=False),
        mpf.make_addplot(df_all['BBM'], panel=0, type='line', secondary_y=False),
        mpf.make_addplot(df_all['BBU'], panel=0, type='line', secondary_y=False),
        ]

mpf.plot(ohcl_squeeze,
         volume_panel=2,
         figratio=(4, 1.5),
         figscale=3.5,
         style='charles',
         type='candle',
         addplot=apds,
         returnfig=True)

st.pyplot()
