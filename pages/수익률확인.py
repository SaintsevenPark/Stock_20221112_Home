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


upload_file = st.file_uploader("CSV 선택")
st.text(upload_file)

if upload_file:
    df = pd.read_csv(upload_file)
    df.drop(df.columns[0], axis=1, inplace=True)

    # Current price 확인
    current_price = []
    for i in range(len(df)):
        df_current = fdr.DataReader(df['Symbol'].iloc[i], '2022-11')
        current_price.append(df_current['Close'].iloc[-1])
        time.sleep(0.3)

    df['현재가'] = current_price
    df['차액'] = df['현재가'] - df['Price']
    df['수익률'] = (df['차액'] / df['Price']) * 100

    st.dataframe(df)
