import pandas_ta as pt
import numpy as np


def get_indicator(df):
    bb = pt.bbands(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    df['BBL'] = bb[f"{bb.columns[0]}"]
    df['BBM'] = bb[f"{bb.columns[1]}"]
    df['BBU'] = bb[f"{bb.columns[2]}"]
    df['BBB'] = bb[f"{bb.columns[3]}"]
    df['BBP'] = bb[f"{bb.columns[4]}"]
    # MACD
    macd = pt.macd(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['MACD'] = macd[f"{macd.columns[0]}"]
    df['MACDh'] = macd[f"{macd.columns[1]}"]
    df['MACDs'] = macd[f"{macd.columns[2]}"]
    df['MFI'] = pt.mfi(df['High'], df['Low'], df['Close'], df['Volume'], timeperiod=14)
    df['RSI'] = pt.rsi(df['Close'], timeperiod=14)
    #
    df['변화량'] = df['Close'] - df['Close'].shift(1)
    df['상승폭'] = np.where(df['변화량'] >= 0, df['변화량'], 0)
    df['하락폭'] = np.where(df['변화량'] < 0, df['변화량'].abs(), 0)

    # Stochastic
    stochastic = pt.stoch(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    df['STOCHk'] = stochastic[f"{stochastic.columns[0]}"]
    df['STOCHd'] = stochastic[f"{stochastic.columns[1]}"]

    df['willR'] = pt.willr(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['CCI'] = pt.cci(df['High'], df['Low'], df['Close'], timeperiod=14)
    # 단순 이동평균선
    df['SMA5'] = pt.sma(df['Close'], 5)
    df['SMA10'] = pt.sma(df['Close'], 10)
    df['SMA20'] = pt.sma(df['Close'], 20)
    df['SMA60'] = pt.sma(df['Close'], 60)
    df['SMA120'] = pt.sma(df['Close'], 120)
    # SuperTrend
    supert = pt.supertrend(df['High'], df['Low'], df['Close'], length=10, multiplier=4.0)
    df['SUPERT'] = supert[f"{supert.columns[0]}"]
    df['SUPERTd'] = supert[f"{supert.columns[1]}"]
    df['SUPERTl'] = supert[f"{supert.columns[2]}"]
    df['SUPERTs'] = supert[f"{supert.columns[3]}"]
    # CCI
    df['CCI'] = pt.cci(df['High'], df['Low'], df['Close'], length=14)
    # Trix 지표
    trix = pt.trix(df['Close'], timeperiod=20)
    df['TRIX'] = trix[f"{trix.columns[0]}"]
    df['TRIXs'] = trix[f"{trix.columns[1]}"]

    return df