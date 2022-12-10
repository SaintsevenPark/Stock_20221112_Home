import pandas_ta as pt
import numpy as np
import pandas as pd


def get_indicator(df, l_line, s_line):
    # BOLLINGER BAND
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
    df['SUPERTp'] = ((df['Close'] - df['SUPERT']) / df['Close']) * 100
    df['SUPERTlp'] = df['SUPERTl'] * (1 + (l_line / 100))
    df['SUPERTsp'] = df['SUPERTs'] * (1 + (s_line / 100))

    # Triple SuperTrend 10 - 11 - 12    1 - 2 - 3
    supert10 = pt.supertrend(df['High'], df['Low'], df['Close'], length=10, multiplier=1.0)
    df['SUPERT10'] = supert10[f"{supert10.columns[0]}"]
    df['SUPERTd10'] = supert10[f"{supert10.columns[1]}"]
    df['SUPERTl10'] = supert10[f"{supert10.columns[2]}"]
    df['SUPERTs10'] = supert10[f"{supert10.columns[3]}"]

    supert11 = pt.supertrend(df['High'], df['Low'], df['Close'], length=11, multiplier=2.0)
    df['SUPERT11'] = supert11[f"{supert11.columns[0]}"]
    df['SUPERTd11'] = supert11[f"{supert11.columns[1]}"]
    df['SUPERTl11'] = supert11[f"{supert11.columns[2]}"]
    df['SUPERTs11'] = supert11[f"{supert11.columns[3]}"]

    supert12 = pt.supertrend(df['High'], df['Low'], df['Close'], length=12, multiplier=3.0)
    df['SUPERT12'] = supert12[f"{supert12.columns[0]}"]
    df['SUPERTd12'] = supert12[f"{supert12.columns[1]}"]
    df['SUPERTl12'] = supert12[f"{supert12.columns[2]}"]
    df['SUPERTs12'] = supert12[f"{supert12.columns[3]}"]

    # Stochastic RSI
    stochrsi = pt.stochrsi(close=df['Close'], length=14, rsi_length=14, k=3, d=3)
    df['STOCHRSIk'] = stochrsi[f"{stochrsi.columns[0]}"]
    df['STOCHRSId'] = stochrsi[f"{stochrsi.columns[1]}"]

    # EMA200
    df['EMA200'] = pt.ema(close=df['Close'], length=200, offset=0)

    # CCI
    df['CCI'] = pt.cci(df['High'], df['Low'], df['Close'], length=14)
    # Trix 지표
    trix = pt.trix(df['Close'], timeperiod=20)
    df['TRIX'] = trix[f"{trix.columns[0]}"]
    df['TRIXs'] = trix[f"{trix.columns[1]}"]

    return df


def heikin_ashi(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['Open', 'High', 'Low', 'Close'])

    heikin_ashi_df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4

    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['Open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i - 1, 0] + heikin_ashi_df.iat[i - 1, 3]) / 2

    heikin_ashi_df['High'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['High']).max(axis=1)

    heikin_ashi_df['Low'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['Low']).min(axis=1)

    return heikin_ashi_df



def get_squeeze_momentum(df):
    length = 20
    mult = 2
    length_KC = 20
    mult_KC = 1.5



    # calculate Bollinger Bands
    # moving average
    m_avg = df['Close'].rolling(window=length).mean()
    # standard deviation
    m_std = df['Close'].rolling(window=length).std(ddof=0)
    # upper Bollinger Bands
    df['upper_BB'] = m_avg + mult * m_std
    # lower Bollinger Bands
    df['lower_BB'] = m_avg - mult * m_std

    # calculate Keltner Channel
    # first we need to calculate True Range
    df['tr0'] = abs(df["High"] - df["Low"])
    df['tr1'] = abs(df["High"] - df["Close"].shift())
    df['tr2'] = abs(df["Low"] - df["Close"].shift())
    df['tr'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)
    # moving average of the TR
    range_ma = df['tr'].rolling(window=length_KC).mean()
    # upper Keltner Channel
    df['upper_KC'] = m_avg + range_ma * mult_KC
    # lower Keltner Channel
    df['lower_KC'] = m_avg - range_ma * mult_KC

    # check for 'squeeze'
    df['squeeze_on'] = (df['lower_BB'] > df['lower_KC']) & (df['upper_BB'] < df['upper_KC'])


    df['squeeze_off'] = (df['lower_BB'] < df['lower_KC']) & (df['upper_BB'] > df['upper_KC'])

    # calculate momentum value
    highest = df['High'].rolling(window=length_KC).max()
    lowest = df['Low'].rolling(window=length_KC).min()
    m1 = (highest + lowest) / 2
    df['value'] = (df['Close'] - (m1 + m_avg) / 2)
    fit_y = np.array(range(0, length_KC))
    df['value'] = df['value'].rolling(window=length_KC).apply(lambda x: np.polyfit(fit_y, x, 1)[0] * (length_KC - 1) +
                     np.polyfit(fit_y, x, 1)[1], raw=True)

    # check for 'squeeze'
    df['squeeze_on'] = (df['lower_BB'] > df['lower_KC']) & (df['upper_BB'] < df['upper_KC'])
    df['squeeze_off'] = (df['lower_BB'] < df['lower_KC']) & (df['upper_BB'] > df['upper_KC'])

    # 아래는 없어도 상관 없는것 같음
    # # buying window for long position:
    # # 1. black cross becomes gray (the squeeze is released)
    # long_cond1 = (df['squeeze_off'][-2] == False) & (df['squeeze_off'][-1] == True)
    # # 2. bar value is positive => the bar is light green k
    # long_cond2 = df['value'][-1] > 0
    # enter_long = long_cond1 and long_cond2
    #
    # # buying window for short position:
    # # 1. black cross becomes gray (the squeeze is released)
    # short_cond1 = (df['squeeze_off'][-2] == False) & (df['squeeze_off'][-1] == True)
    # # 2. bar value is negative => the bar is light red
    # short_cond2 = df['value'][-1] < 0
    # enter_short = short_cond1 and short_cond2

    # df_squeeze = pt.squeeze(high=df['High'], low=df['Low'], close=df['Close'], bb_length=20, bb_std=None, kc_length=20,
    #            kc_scalar=1.5, mom_length=None, mom_smooth=None, use_tr=None, mamode=None, offset=2)

    return df