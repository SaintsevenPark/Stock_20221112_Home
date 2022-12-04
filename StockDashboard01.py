import pandas as pd
import configparser
import streamlit as st
import FinanceDataReader as fdr
# import matplotlib.pyplot as plt
# import time
# import numpy as np
# import cufflinks as cf
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


# 지수 불러오기
indices = ['KS11', 'KQ11', 'DJI', 'IXIC']
select_indices = st.selectbox('지수', indices)
df_indices = fdr.DataReader(select_indices, '2022')
df_indices = ssl.get_indicator(df_indices)
with st.expander('데이터 프레임'):
    st.dataframe(df_indices)

fig = df_indices[['Close', 'SUPERTl', 'SUPERTs']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="일간 가격 변동")
st.plotly_chart(fig)

fig = df_indices[['STOCHRSIk', 'STOCHRSId']].iplot(asFigure=True, xTitle="The X Axis",
                        yTitle="The Y Axis", title="일간 가격 변동")
st.plotly_chart(fig)