import pandas as pd
import streamlit as st
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
st.set_page_config(page_title=None, page_icon="chart_with_upwards_trend", layout="wide", initial_sidebar_state="auto", menu_items=None)

l_line = 2
s_line = -10
stock_count = 500
default_strategy = 8
start_year = '2021'

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

