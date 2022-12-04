import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import time
import numpy as np
import seaborn as sns
import pandas_ta as pt

from plotly.subplots import make_subplots
#
from saintsevenlib import saintsevenlib as ssl
from saintsevenlib import saintsevenstrategy as sst



stock_count = 100

df_stocklist = pd.DataFrame()
df_stocklistfile = pd.read_csv('stocklist_krx.csv')
df_stocklist['index'] = df_stocklistfile[0:stock_count].index
df_stocklist['Code'] = df_stocklistfile[0:stock_count]['Code']
df_stocklist['Name'] = df_stocklistfile[0:stock_count]['Name']
df_stocklist['Close'] = df_stocklistfile[0:stock_count]['Close']

number = st.sidebar.number_input('Insert a number', min_value=0, max_value=stock_count)

tick_code = df_stocklist['Code'].iloc[number]
df = fdr.DataReader(tick_code, '2022')
df = ssl.get_indicator(df)
stock_code = df_stocklist['Code'].iloc[number]
stock_name = df_stocklist['Name'].iloc[number]
stock_price = df['Close'].iloc[-1]

st.sidebar.markdown(f"### [{stock_code}] {stock_name} : {stock_price}")
with st.sidebar.expander("주식 목록"):
    st.dataframe(df_stocklist)

fig, ax = plt.subplots(figsize=(24, 6))
sns
sns.set(style='ticks')
sns.set_context('paper', font_scale=1, rc={"grid.linewidth": 0.1})
ax = sns.lineplot(x=df.index, y=df['Close'], data=df)
ax = sns.scatterplot(x=df.index, y=df['SUPERTl'])
ax = sns.scatterplot(x=df.index, y=df['SUPERTs'])
st.pyplot(fig)

# 스타일 꾸미는 방법
# https://hleecaster.com/python-seaborn-set-style-and-context/
# fig, ax = plt.subplots()
# >>> ax.scatter([1, 2, 3], [1, 2, 3])
# >>>    ... other plotting actions ...
# >>> st.pyplot(fig)

# {'axes.labelsize': 17.6,
#  'axes.titlesize': 19.200000000000003,
#  'font.size': 19.200000000000003,
#  'grid.linewidth': 1.6,
#  'legend.fontsize': 16.0,
#  'lines.linewidth': 2.8000000000000003,
#  'lines.markeredgewidth': 0.0,
#  'lines.markersize': 11.200000000000001,
#  'patch.linewidth': 0.48,
#  'xtick.labelsize': 16.0,
#  'xtick.major.pad': 11.200000000000001,
#  'xtick.major.width': 1.6,
#  'xtick.minor.width': 0.8,
#  'ytick.labelsize': 16.0,
#  'ytick.major.pad': 11.200000000000001,
#  'ytick.major.width': 1.6,
#  'ytick.minor.width': 0.8}

# sns.set_context() 안에 총 4종류의 스케일(사이즈)를 선택할 수 있다. paper, notebook, talk, poster. 여기서 기본값은 notebook이다.
# *** Built-in Themes (내장 테마) 활용하기
# Seaborn에는 5가지 기본 제공 테마가 있다. darkgrid, whitegrid, dark, white, ticks. 기본값은 darkgrid이지만, 원하는대로 변경이 가능하다.