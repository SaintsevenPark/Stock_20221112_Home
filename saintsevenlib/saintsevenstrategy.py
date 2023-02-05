import numpy as np
import pandas as pd
import saintsevenlib as ssl


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


# -----------------------------   전략 1 ---------------------------------------
# 5 이평선이 20 이평선 아래에서 V 자 반등 할고 rsi가 우상 mfi가 우상
def strategy01(df):
    buy, sell, superbuy, supersell = [], [], [], []
    trigger = False
    for i in range(2, len(df)):
        if df['SMA20'].iloc[i] > df['SMA5'].iloc[i] > df['SMA5'].iloc[i - 1] \
                and df['SMA5'].iloc[i - 1] <= df['SMA5'].iloc[i - 2] < df['SMA5'].iloc[i - 3] \
                and df['RSI'].iloc[i] > df['RSI'].iloc[i - 1] \
                and df['MFI'].iloc[i] > df['MFI'].iloc[i - 1]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True

        elif df['SMA5'].iloc[i] < df['SMA20'].iloc[i] < df['SMA5'].iloc[i - 1] \
                and df['SMA5'].iloc[i - 1] < df['SMA5'].iloc[i - 2] \
                and df['SMA5'].iloc[i - 2] < df['SMA5'].iloc[i - 3] \
                and df['RSI'].iloc[i] < df['RSI'].iloc[i - 1] \
                and df['MFI'].iloc[i] < df['MFI'].iloc[i - 1]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False

        if df['SUPERTs'][i - 1] > df['Close'].iloc[i - 1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i - 1] < df['Close'].iloc[i - 1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)
    desc = '5 이평선이 20 이평선 아래에서 V 자 반등 할고 rsi가 우상 mfi가 우상'

    return buy, sell, superbuy, supersell, desc


# -----------------------------   전략 2 ---------------------------------------
# RSI 지표가 50을 돌파 할때 매수 50을 하락 할때 매도
def strategy02(df):
    buy, sell, superbuy, supersell = [], [], [], []
    # trigger = False
    for i in range(2, len(df)):
        if df['RSI'].iloc[i] > 50 > df['RSI'].iloc[i - 1] > df['RSI'].iloc[i - 2]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True
        elif df['RSI'].iloc[i] < 50 < df['RSI'].iloc[i - 1] < df['RSI'].iloc[i - 2]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False

        if df['SUPERTs'][i - 1] > df['Close'].iloc[i - 1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i - 1] < df['Close'].iloc[i - 1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = 'RSI 지표가 50을 돌파 할때 매수 50을 하락 할때 매도'

    return buy, sell, superbuy, supersell, desc


# -----------------------------   전략 3 ---------------------------------------
# 5 이평선이 20 이평선을 돌파 할때
def strategy03(df):
    buy, sell, superbuy, supersell = [], [], [], []
    trigger = False
    for i in range(2, len(df)):
        if df['SMA5'].iloc[i] > df['SMA20'].iloc[i] \
                and df['SMA5'].iloc[i - 1] < df['SMA20'].iloc[i - 1] \
                and df['SMA5'].iloc[i - 2] < df['SMA20'].iloc[i - 2]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True
        elif df['SMA5'].iloc[i] < df['SMA20'].iloc[i] \
                and df['SMA5'].iloc[i - 1] > df['SMA20'].iloc[i - 1] \
                and df['SMA5'].iloc[i - 2] > df['SMA20'].iloc[i - 2]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False
        if df['SUPERTs'][i - 1] > df['Close'].iloc[i - 1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i - 1] < df['Close'].iloc[i - 1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = '5 이평선이 20 이평선을 돌파 할때'
    return buy, sell, superbuy, supersell, desc


# -----------------------------   전략 4 ---------------------------------------
# 5 이평선이 20 이평선 아래에서 V 자 반등 할때
def strategy04(df):
    buy, sell, superbuy, supersell = [], [], [], []
    for i in range(2, len(df)):
        if df['SMA20'].iloc[i] > df['SMA5'].iloc[i] > df['SMA5'].iloc[i - 1] \
                and df['SMA5'].iloc[i - 1] <= df['SMA5'].iloc[i - 2] \
                and df['SMA5'].iloc[i - 2] < df['SMA5'].iloc[i - 3]:
            buy.append(i)
        elif df['SMA20'].iloc[i] < df['SMA5'].iloc[i] < df['SMA5'].iloc[i - 1] \
                and df['SMA5'].iloc[i - 1] >= df['SMA5'].iloc[i - 2] \
                and df['SMA5'].iloc[i - 2] > df['SMA5'].iloc[i - 3]:
            sell.append(i)
        if df['SUPERTs'][i - 1] > df['Close'].iloc[i - 1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i - 1] < df['Close'].iloc[i - 1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = '5 이평선이 20 이평선 아래에서 V 자 반등 할때'

    return buy, sell, superbuy, supersell, desc


# -----------------------------   전략 5 ---------------------------------------
# # 5 이평선이 20 이평선 아래에서 V 자 반등 할때 rsi가 지정수 이상 일때
def strategy05(df):
    buy, sell, superbuy, supersell = [], [], [], []
    for i in range(2, len(df)):
        if df['SMA20'].iloc[i] > df['SMA5'].iloc[i] > df['SMA5'].iloc[i - 1] \
                and df['SMA5'].iloc[i - 1] <= df['SMA5'].iloc[i - 2] \
                and df['SMA5'].iloc[i - 2] < df['SMA5'].iloc[i - 3] \
                and df['RSI'].iloc[i] > df['RSI'].iloc[i - 1] > 30:
            buy.append(i)
        elif df['SMA20'].iloc[i] < df['SMA5'].iloc[i] < df['SMA5'].iloc[i - 1] \
                and df['SMA5'].iloc[i - 1] >= df['SMA5'].iloc[i - 2] \
                and df['SMA5'].iloc[i - 2] > df['SMA5'].iloc[i - 3]:
            sell.append(i)
        if df['SUPERTs'][i - 1] > df['Close'].iloc[i - 1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i - 1] < df['Close'].iloc[i - 1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = '5 이평선이 20 이평선 아래에서 V 자 반등 할때 rsi가 지정수 이상 일때'

    return buy, sell, superbuy, supersell, desc


# -----------------------------   전략 6 ---------------------------------------
# mfi 가 50이상에서 macd가 골든 크로스 할때
def strategy06(df):
    buy, sell, superbuy, supersell = [], [], [], []
    # trigger = False
    for i in range(2, len(df)):
        if df['MFI'].iloc[i] > df['MFI'].iloc[i - 1] > 50 \
                and df['MACD'].iloc[i] > df['MACD'].iloc[i - 1] \
                and df['MACD'].iloc[i] > df['MACDs'].iloc[i] \
                and df['MACD'].iloc[i - 1] < df['MACDs'].iloc[i - 1]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True
        elif df['MFI'].iloc[i - 1] > df['MFI'].iloc[i] \
                and df['MACD'].iloc[i] < df['MACD'].iloc[i - 1] \
                and df['MACD'].iloc[i] < df['MACDs'].iloc[i] \
                and df['MACD'].iloc[i - 1] > df['MACDs'].iloc[i - 1]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False
        if df['SUPERTs'][i - 1] > df['Close'].iloc[i - 1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i - 1] < df['Close'].iloc[i - 1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = 'mfi 가 50이상에서 macd가 골든 크로스 할때'

    return buy, sell, superbuy, supersell, desc


# -----------------------------   전략 7 ---------------------------------------
def strategy07(df):
    buy, sell, superbuy, supersell = [], [], [], []
    # trigger = False
    for i in range(2, len(df)):
        if df['TRIX'].iloc[i] > 0 > df['TRIX'].iloc[i - 1]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True
        elif df['TRIX'].iloc[i] < 0 < df['TRIX'].iloc[i - 1]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False
        if df['SUPERTs'][i - 1] > df['Close'].iloc[i - 1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i - 1] < df['Close'].iloc[i - 1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = 'TRIX가 0을 돌파할때'

    return buy, sell, superbuy, supersell, desc


# -----------------------------   전략 8 ---------------------------------------
def strategy08(df):
    buy, sell, superbuy, supersell = [], [], [], []
    # trigger = False
    for i in range(2, len(df)):
        if df['TRIX'].iloc[i] > df['TRIXs'].iloc[i] \
                and df['TRIX'].iloc[i - 1] < df['TRIXs'].iloc[i - 1]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True
        elif df['TRIX'].iloc[i] < df['TRIXs'].iloc[i] \
                and df['TRIX'].iloc[i - 1] > df['TRIXs'].iloc[i - 1]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False
        if df['SUPERTs'][i - 1] > df['Close'].iloc[i - 1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i - 1] < df['Close'].iloc[i - 1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = 'TRIX가 TRIXs 을 돌파할때---------------- (0 이상 0이하 로 시도 해볼것.,)'

    return buy, sell, superbuy, supersell, desc


# --------------------------------- 전략 9 -----------------------------------------
def strategy09(df):
    buy, sell, superbuy, supersell = [], [], [], []
    l_line = 2
    s_line = -10

    # SUPERTd 가 1일때가 SUPERTl이 종가보다 아래에 있고 값이 있슴 -> l
    # SUPERTd 가 -1일때가 SUPERTs가 종가보다 위에 있고 값이 있슴 -> s

    for i in range(2, len(df)):
        if df['SUPERTd'].iloc[i] > 0:
            if df['Close'].iloc[i] >= df['SUPERTlp'].iloc[i] > df['Close'].iloc[i - 1]:
                buy.append(i)
            if df['SUPERTlp'].iloc[i] < (l_line + 12) < df['SUPERTlp'].iloc[i - 1]:
                sell.append(i)
        elif df['SUPERTd'].iloc[i] < 0:
            if df['Close'].iloc[i] >= df['SUPERTsp'].iloc[i] > df['Close'].iloc[i - 1]:
                buy.append(i)

    desc = f'SuperT 지표이용,  SUPERTl(1)구간일때 종가가 `{l_line}`을 우상향 SUPERs(-1)구간일때 종가가 `{s_line}`을 우상향할때 매수'

    return buy, sell, superbuy, supersell, desc


# --------------------------------- 전략 10 -----------------------------------------
def strategy10(df):
    buy, sell, superbuy, supersell = [], [], [], []
    l_line = 2
    s_line = -10

    # SUPERTd 가 1일때가 SUPERTl이 종가보다 아래에 있고 값이 있슴 -> l
    # SUPERTd 가 -1일때가 SUPERTs가 종가보다 위에 있고 값이 있슴 -> s

    for i in range(2, len(df)):
        if df['SUPERTd'].iloc[i] > 0:
            if df['SUPERTlp'].iloc[i] > l_line > df['SUPERTlp'].iloc[i - 1] \
                    and 30 > df['STOCHRSIk'].iloc[i] > df['STOCHRSIk'].iloc[i - 1] \
                    and 30 > df['STOCHRSId'].iloc[i] > df['STOCHRSId'].iloc[i - 1]:
                buy.append(i)
            # if df['SUPERTp'].iloc[i] < (l_line * 6) < df['SUPERTp'].iloc[i-1]:
            #     sell.append(i)
        elif df['SUPERTd'].iloc[i] < 0:
            if df['SUPERTsp'].iloc[i] > s_line > df['SUPERTsp'].iloc[i - 1] \
                    and df['SUPERTs'].iloc[i] == df['SUPERTs'].iloc[i - 1] == df['SUPERTs'].iloc[i - 2] \
                    and 30 > df['STOCHRSIk'].iloc[i] > df['STOCHRSIk'].iloc[i - 1] \
                    and 30 > df['STOCHRSId'].iloc[i] > df['STOCHRSId'].iloc[i - 1]:
                buy.append(i)

    desc = f'SuperT 지표이용,  SUPERTl(1)구간일때 종가가 `{l_line}`을 우상향 SUPERs(-1)구간일때 종가가 `{s_line}`을 우상향 하며' \
           f'Stochastic RSI가 20이 이하에서 상승중일때 매수'

    return buy, sell, superbuy, supersell, desc


# --------------------------------- 전략 11 -----------------------------------------
def strategy11(df):
    buy, sell, superbuy, supersell = [], [], [], []

    # SUPERTd 가 1일때가 SUPERTl이 종가보다 아래에 있고 값이 있슴 -> l
    # SUPERTd 가 -1일때가 SUPERTs가 종가보다 위에 있고 값이 있슴 -> s

    for i in range(len(df)):
        if df['SUPERTd'].iloc[i] > 0:
            if df['Close'].iloc[i] >= df['SUPERTlp'].iloc[i] > df['Close'].iloc[i - 1]:
                buy.append(i)
            # if df['SUPERTp'].iloc[i] < (l_line * 6) < df['SUPERTp'].iloc[i-1]:
            #     sell.append(i)
        elif df['SUPERTd'].iloc[i] < 0:
            if (df['SUPERTs'].iloc[i] == df['SUPERTs'].iloc[i - 1] == df['SUPERTs'].iloc[i - 2] == df['SUPERTs'].iloc[
                i - 3] \
                and df['Close'].iloc[i - 1] < df['Close'].iloc[i] <= df['SUPERTsp'].iloc[i]) \
                    or (df['SUPERTs'].iloc[i] == df['SUPERTs'].iloc[i - 1] == df['SUPERTs'].iloc[i - 2] <
                        df['SUPERTs'].iloc[i - 3] \
                        and df['Close'].iloc[i - 1] < df['Close'].iloc[i] <= df['SUPERTsp'].iloc[i]):
                # and df['STOCHRSIk'].iloc[i] > df['STOCHRSIk'].iloc[i-1]:
                buy.append(i)

    desc = f'[전략11] SuperT 지표이용,  SUPERTl(1)구간일때는 종가가 Supertl를 접근했다가 우상향, SUPERs(-1)구간일때 Superts 가 내려가다가 수평으로 바뀔때매수'

    return buy, sell, superbuy, supersell, desc


# --------------------------------- 전략 12 -----------------------------------------
def strategy12(df):
    buy, sell, superbuy, supersell = [], [], [], []

    df_squeeze = get_squeeze_momentum(df=df)
    df_heikinashi = heikin_ashi(df=df)

    for i in range(len(df_squeeze)):
        if 0 > df_squeeze['value'].iloc[i] > df_squeeze['value'].iloc[i - 1] > df_squeeze['value'].iloc[i - 2] < df_squeeze['value'].iloc[i - 3]:
            if df_heikinashi['Open'].iloc[i] < df_heikinashi['Close'].iloc[i]\
                    and df_heikinashi['Open'].iloc[i-1] < df_heikinashi['Close'].iloc[i-1]:
                buy.append(i)

    desc = f'Squeeze 모멘텀을 이용한 전략'

    return buy, sell, superbuy, supersell, desc
