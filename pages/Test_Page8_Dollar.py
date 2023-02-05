import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import numpy as np
import mplfinance as mpf

import cufflinks as cf
import plotly.graph_objs as go

from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst

# -------------------- 페이지 형태 최기화
st.set_page_config(page_title=None, page_icon="chart_with_upwards_trend", layout="wide", initial_sidebar_state="auto", menu_items=None)

l_line = 2
s_line = -8
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

st.sidebar.markdown("## 환률")
selected_strategy = st.sidebar.selectbox("전략 선택", strategy_names_to_funcs.keys(), index=default_strategy)

df_origin = fdr.DataReader('USD/KRW', start=start_year)
df_heiken = ssl.heikin_ashi(df_origin).astype(int)
df_squeeze = ssl.get_squeeze_momentum(df_origin)

# -----------------------------------------------------------------------
# with st.expander("순수 데이터 프레임"):
#     st.dataframe(df_origin)
# with st.expander("Heiken Ashi 데이터 프레임"):
#     st.dataframe(df_heiken)
# with st.expander("Squeeze 데이터 프레임"):
#     st.dataframe(df_squeeze)
df = ssl.get_indicator(df_origin, l_line, s_line)
# with st.expander("모든 지표"):
#     st.dataframe(df)


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

# =================== 필요한 정보만 정리해서 DataFrame 을 만듦
df_just = pd.DataFrame()
df_just['Open'] = df_origin['Open']
df_just['High'] = df_origin['High']
df_just['Low'] = df_origin['Low']
df_just['Close'] = df_origin['Close']
df_just['Open_HI'] = df_heiken['Open']
df_just['High_HI'] = df_heiken['High']
df_just['Low_HI'] = df_heiken['Low']
df_just['Close_HI'] = df_heiken['Close']
df_just['SUPERTl'] = df['SUPERTl']
df_just['SUPERTs'] = df['SUPERTs']
df_just['SUPERTlp'] = df['SUPERTlp']
df_just['SUPERTsp'] = df['SUPERTsp']
df_just['STOCHRSIk'] = df['STOCHRSIk']
df_just['STOCHRSId'] = df['STOCHRSId']
df_just['SMA5'] = df['SMA5']
df_just['SMA20'] = df['SMA20']
df_just['SQ_value'] = df['value']
df_just['squeeze_off'] = df['squeeze_off']
df_just['squeeze_on'] = df['squeeze_on']

df_just['Buy'] = df['Buy']
df_just['Sell'] = df['Sell']
with st.expander("필요한 지표만"):
    st.dataframe(df_just)
# ======================================================


# -----------------------  Plotly 시작
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
                      legendgroup='종가'
                      )
trace1_3 = go.Scatter(x=df_origin.index,
                      y=df_just['SUPERTs'],
                      name='슈퍼트렌드 s',
                      legendgroup='종가'
                      )
trace1_4 = go.Scatter(x=df_just.index,
                      y=df_just['SUPERTlp'],
                      name='슈퍼트렌드 l %',
                      legendgroup='종가',
                      line=dict(width=0.5)
                      )
trace1_5 = go.Scatter(x=df_just.index,
                      y=df_just['SUPERTsp'],
                      name='슈퍼트렌드 s %',
                      legendgroup='종가',
                      line=dict(width=0.5)
                      )
trace1_6 = go.Scatter(x=df_just.index,
                      y=df_just['Buy'],
                      name='Buy',
                      legendgroup='종가',
                      mode='markers',
                      marker=dict(
                          color='red',
                          size=10,
                          line=dict(
                              color='MediumPurple',
                              width=3
                          ))
                      )

# 2 - Stochastic
trace2_1 = go.Scatter(x=df_just.index,
                      y=df_just['STOCHRSIk'],
                      name='StochasticRSI K',
                      legendgroup='StochasticRSI K'
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

# 4. Heiken Ashi
trace4_1 = go.Candlestick(x=df_just.index,
                          open=df_just['Open_HI'],
                          high=df_just['High_HI'],
                          low=df_just['Low_HI'],
                          close=df_just['Close_HI'],
                          name='Heiken Ashi',
                          legendgroup='Heiken Ashi',
                          legendrank=4,
                          increasing_line_color='red',
                          decreasing_line_color='green',
                          )
trace4_2 = go.Scatter(x=df_just.index,
                      y=df_just['Buy'] * 1.05,
                      name='Buy',
                      legendgroup='Heiken Ashi',
                      legendrank=4,
                      mode='markers',
                      marker=dict(
                          color='red',
                          size=10,
                          line=dict(
                              color='MediumPurple',
                              width=3
                          ))
                      )

# 5. Squeeze
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
trace5_1 = go.Bar(x=df_just.index,
                      y=df_just['SQ_value'],
                      name='Candle Stick',
                  marker=dict(color=colors),
                      legendgroup='Candle Stick',
                      legendrank=5
                      )
trace5_2 = go.Scatter(x=df_just.index,
                      y=df_just['Buy'] * 0,
                      name='Buy',
                      legendgroup='Candle Stick',
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
# trace5_3 = go.Scatter(x=df_just.index,
#                       y=df_just['Buy'] * 1.05,
#                       name='Buy',
#                       mode='markers',
#                       marker=dict(
#                           color='red',
#                           size=10,
#                           line=dict(
#                               color='MediumPurple',
#                               width=3
#                           ))
#                       )


data1 = [trace1_1, trace1_2, trace1_3, trace1_4, trace1_5, trace1_6]
data2 = [trace2_1, trace2_2, trace2_3]
data3 = [trace3_1, trace3_2, trace3_3]
data4 = [trace4_1, trace4_2]
data5 = [trace5_1, trace5_2]

fig1 = go.Figure(data=data1)
fig2 = go.Figure(data=data2)
fig3 = go.Figure(data=data3)
fig4 = go.Figure(data=data4)
fig5 = go.Figure(data=data5)

figs = cf.subplots([fig1, fig2, fig3, fig5, fig4], shape=(5, 1))
figs['layout'].update(height=1500, title='PARTICLES CORRELATION', legend_tracegroupgap = 180)
figs['layout'].update(xaxis5=dict(rangeslider=dict(visible=False)))


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
        ]

mpf.plot(ohcl_squeeze,
         volume_panel=2,
         figratio=(4, 1),
         figscale=1.5,
         style='charles',
         type='candle',
         addplot=apds,
         returnfig=True)

st.pyplot()
