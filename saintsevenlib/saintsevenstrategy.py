import numpy as np

# -----------------------------   전략 1 ---------------------------------------
# 5 이평선이 20 이평선 아래에서 V 자 반등 할고 rsi가 우상 mfi가 우상
def strategy01(df):
    buy, sell, superbuy, supersell = [], [], [], []
    trigger = False
    for i in range(2, len(df)):
        if df['SMA20'].iloc[i] > df['SMA5'].iloc[i] > df['SMA5'].iloc[i-1] \
            and df['SMA5'].iloc[i-1] <= df['SMA5'].iloc[i-2] < df['SMA5'].iloc[i-3] \
            and df['RSI'].iloc[i] > df['RSI'].iloc[i-1] \
            and df['MFI'].iloc[i] > df['MFI'].iloc[i-1]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True

        elif df['SMA5'].iloc[i] < df['SMA20'].iloc[i] < df['SMA5'].iloc[i-1] \
            and df['SMA5'].iloc[i-1] < df['SMA5'].iloc[i-2] \
            and df['SMA5'].iloc[i - 2] < df['SMA5'].iloc[i-3] \
            and df['RSI'].iloc[i] < df['RSI'].iloc[i-1] \
            and df['MFI'].iloc[i] < df['MFI'].iloc[i-1]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False

        if df['SUPERTs'][i-1] > df['Close'].iloc[i-1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i-1] < df['Close'].iloc[i-1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
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

        if df['SUPERTs'][i-1] > df['Close'].iloc[i-1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i-1] < df['Close'].iloc[i-1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
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
            and df['SMA5'].iloc[i-1] < df['SMA20'].iloc[i-1] \
            and df['SMA5'].iloc[i-2] < df['SMA20'].iloc[i-2]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True
        elif df['SMA5'].iloc[i] < df['SMA20'].iloc[i] \
            and df['SMA5'].iloc[i-1] > df['SMA20'].iloc[i-1] \
            and df['SMA5'].iloc[i-2] > df['SMA20'].iloc[i-2]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False
        if df['SUPERTs'][i-1] > df['Close'].iloc[i-1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i-1] < df['Close'].iloc[i-1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = '5 이평선이 20 이평선을 돌파 할때'
    return buy, sell, superbuy, supersell, desc


# -----------------------------   전략 4 ---------------------------------------
# 5 이평선이 20 이평선 아래에서 V 자 반등 할때
def strategy04(df):
    buy, sell, superbuy, supersell = [], [], [], []
    for i in range(2, len(df)):
        if df['SMA20'].iloc[i] > df['SMA5'].iloc[i] > df['SMA5'].iloc[i-1] \
                and df['SMA5'].iloc[i-1] <= df['SMA5'].iloc[i-2] \
                and df['SMA5'].iloc[i-2] < df['SMA5'].iloc[i-3]:
            buy.append(i)
        elif df['SMA20'].iloc[i] < df['SMA5'].iloc[i] < df['SMA5'].iloc[i-1] \
                and df['SMA5'].iloc[i-1] >= df['SMA5'].iloc[i-2] \
                and df['SMA5'].iloc[i-2] > df['SMA5'].iloc[i-3]:
            sell.append(i)
        if df['SUPERTs'][i-1] > df['Close'].iloc[i-1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i-1] < df['Close'].iloc[i-1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = '5 이평선이 20 이평선 아래에서 V 자 반등 할때'

    return buy, sell, superbuy, supersell, desc


# -----------------------------   전략 5 ---------------------------------------
# # 5 이평선이 20 이평선 아래에서 V 자 반등 할때 rsi가 지정수 이상 일때
def strategy05(df):
    buy, sell, superbuy, supersell = [], [], [], []
    for i in range(2, len(df)):
        if df['SMA20'].iloc[i] > df['SMA5'].iloc[i] > df['SMA5'].iloc[i-1] \
                and df['SMA5'].iloc[i-1] <= df['SMA5'].iloc[i-2] \
                and df['SMA5'].iloc[i-2] < df['SMA5'].iloc[i-3]\
                and df['RSI'].iloc[i] > df['RSI'].iloc[i-1] > 30:
            buy.append(i)
        elif df['SMA20'].iloc[i] < df['SMA5'].iloc[i] < df['SMA5'].iloc[i-1] \
                and df['SMA5'].iloc[i-1] >= df['SMA5'].iloc[i-2] \
                and df['SMA5'].iloc[i-2] > df['SMA5'].iloc[i-3]:
            sell.append(i)
        if df['SUPERTs'][i-1] > df['Close'].iloc[i-1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i-1] < df['Close'].iloc[i-1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = '5 이평선이 20 이평선 아래에서 V 자 반등 할때 rsi가 지정수 이상 일때'

    return buy, sell, superbuy, supersell, desc

# -----------------------------   전략 6 ---------------------------------------
# mfi 가 50이상에서 macd가 골든 크로스 할때
def strategy06(df):
    buy, sell, superbuy, supersell = [], [], [], []
    # trigger = False
    for i in range(2, len(df)):
        if df['MFI'].iloc[i] > df['MFI'].iloc[i-1] > 50 \
            and df['MACD'].iloc[i] > df['MACD'].iloc[i-1] \
            and df['MACD'].iloc[i] > df['MACDs'].iloc[i] \
            and df['MACD'].iloc[i-1] < df['MACDs'].iloc[i-1]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True
        elif df['MFI'].iloc[i-1] > df['MFI'].iloc[i] \
            and df['MACD'].iloc[i] < df['MACD'].iloc[i-1] \
            and df['MACD'].iloc[i] < df['MACDs'].iloc[i] \
            and df['MACD'].iloc[i-1] > df['MACDs'].iloc[i-1]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False
        if df['SUPERTs'][i-1] > df['Close'].iloc[i-1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i - 1] < df['Close'].iloc[i-1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = 'mfi 가 50이상에서 macd가 골든 크로스 할때'

    return buy, sell, superbuy, supersell, desc

# -----------------------------   전략 7 ---------------------------------------
def strategy07(df):
    buy, sell, superbuy, supersell = [], [], [], []
    # trigger = False
    for i in range(2, len(df)):
        if df['TRIX'].iloc[i] > 0 > df['TRIX'].iloc[i-1]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True
        elif df['TRIX'].iloc[i] < 0 < df['TRIX'].iloc[i-1]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False
        if df['SUPERTs'][i-1] > df['Close'].iloc[i-1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i-1] < df['Close'].iloc[i-1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = 'TRIX가 0을 돌파할때'

    return buy, sell, superbuy, supersell, desc

# -----------------------------   전략 8 ---------------------------------------
def strategy08(df):
    buy, sell, superbuy, supersell = [], [], [], []
    # trigger = False
    for i in range(2, len(df)):
        if df['TRIX'].iloc[i] > df['TRIXs'].iloc[i] \
           and df['TRIX'].iloc[i-1] < df['TRIXs'].iloc[i-1]:
            buy.append(i)
            # if trigger == False:
            #     buy.append(i)
            #     trigger = True
        elif df['TRIX'].iloc[i] < df['TRIXs'].iloc[i] \
           and df['TRIX'].iloc[i-1] > df['TRIXs'].iloc[i-1]:
            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False
        if df['SUPERTs'][i-1] > df['Close'].iloc[i-1] and df['SUPERTl'][i] < df['Close'].iloc[i]:
            superbuy.append(i)
        elif df['SUPERTl'][i-1] < df['Close'].iloc[i-1] and df['SUPERTs'][i] > df['Close'].iloc[i]:
            supersell.append(i)

    desc = 'TRIX가 TRIXs 을 돌파할때---------------- (0 이상 0이하 로 시도 해볼것.,)'

    return buy, sell, superbuy, supersell, desc


# --------------------------------- 전략 9 -----------------------------------------
def strategy09(df, l_line, s_line):
    buy, sell, superbuy, supersell = [], [], [], []

    # SUPERTd 가 1일때가 SUPERTl이 종가보다 아래에 있고 값이 있슴 -> l
    # SUPERTd 가 -1일때가 SUPERTs가 종가보다 위에 있고 값이 있슴 -> s
    df['SUPERTlp'] = df['SUPERTl'] * (1 + (l_line / 100))
    df['SUPERTsp'] = df['SUPERTs'] * (1 + (s_line / 100))

    for i in range(2, len(df)):
        if df['SUPERTd'].iloc[i] > 0:
            if df['Close'].iloc[i] >= df['SUPERTlp'].iloc[i] > df['Close'].iloc[i-1]:
                buy.append(i)
            if df['SUPERTp'].iloc[i] < (l_line + 12) < df['SUPERTp'].iloc[i-1]:
                sell.append(i)
        elif df['SUPERTd'].iloc[i] < 0:
            if df['Close'].iloc[i] >= df['SUPERTsp'].iloc[i] > df['Close'].iloc[i-1]:
                buy.append(i)

    desc = f'SuperT 지표이용,  SUPERTl(1)구간일때 종가가 `{l_line}`을 우상향 SUPERs(-1)구간일때 종가가 `{s_line}`을 우상향할때 매수'

    return buy, sell, superbuy, supersell, desc


# --------------------------------- 전략 10 -----------------------------------------
def strategy10(df, l_line, s_line):
    buy, sell, superbuy, supersell = [], [], [], []

    # SUPERTd 가 1일때가 SUPERTl이 종가보다 아래에 있고 값이 있슴 -> l
    # SUPERTd 가 -1일때가 SUPERTs가 종가보다 위에 있고 값이 있슴 -> s

    df['SUPERTp'] = ((df['Close'] - df['SUPERT']) / df['Close']) * 100

    for i in range(2, len(df)):
        if df['SUPERTd'].iloc[i] > 0:
            if df['SUPERTp'].iloc[i] > l_line > df['SUPERTp'].iloc[i-1]\
                    and 30 > df['STOCHRSIk'].iloc[i] > df['STOCHRSIk'].iloc[i-1]\
                    and 30 > df['STOCHRSId'].iloc[i] > df['STOCHRSId'].iloc[i-1]:
                buy.append(i)
            # if df['SUPERTp'].iloc[i] < (l_line * 6) < df['SUPERTp'].iloc[i-1]:
            #     sell.append(i)
        elif df['SUPERTd'].iloc[i] < 0:
            if df['SUPERTp'].iloc[i] > s_line > df['SUPERTp'].iloc[i - 1] \
                and df['SUPERTs'].iloc[i] == df['SUPERTs'].iloc[i - 1]  == df['SUPERTs'].iloc[i - 2] \
                and 30 > df['STOCHRSIk'].iloc[i] > df['STOCHRSIk'].iloc[i-1] \
                and 30 > df['STOCHRSId'].iloc[i] > df['STOCHRSId'].iloc[i - 1]:
                buy.append(i)

    desc = f'SuperT 지표이용,  SUPERTl(1)구간일때 종가가 `{l_line}`을 우상향 SUPERs(-1)구간일때 종가가 `{s_line}`을 우상향 하며' \
           f'Stochastic RSI가 20이 이하에서 상승중일때 매수'

    return buy, sell, superbuy, supersell, desc

# --------------------------------- 전략 11 -----------------------------------------
def strategy11(df, l_line, s_line):
    buy, sell, superbuy, supersell = [], [], [], []

    # SUPERTd 가 1일때가 SUPERTl이 종가보다 아래에 있고 값이 있슴 -> l
    # SUPERTd 가 -1일때가 SUPERTs가 종가보다 위에 있고 값이 있슴 -> s

    df['SUPERTlp'] = df['SUPERTl'] * (1 + (l_line / 100))
    df['SUPERTsp'] = df['SUPERTs'] * (1 + (s_line / 100))

    for i in range(len(df)):
        if df['SUPERTd'].iloc[i] > 0:
            if df['Close'].iloc[i] >= df['SUPERTlp'].iloc[i] > df['Close'].iloc[i-1]:
                buy.append(i)
            # if df['SUPERTp'].iloc[i] < (l_line * 6) < df['SUPERTp'].iloc[i-1]:
            #     sell.append(i)
        elif df['SUPERTd'].iloc[i] < 0:
            if (df['SUPERTs'].iloc[i] == df['SUPERTs'].iloc[i-1] == df['SUPERTs'].iloc[i-2] == df['SUPERTs'].iloc[i-3] \
                    and df['Close'].iloc[i-1] < df['Close'].iloc[i] <= df['SUPERTsp'].iloc[i]) \
                or (df['SUPERTs'].iloc[i] == df['SUPERTs'].iloc[i-1] == df['SUPERTs'].iloc[i-2] < df['SUPERTs'].iloc[i-3] \
                    and df['Close'].iloc[i-1] < df['Close'].iloc[i] <= df['SUPERTsp'].iloc[i]):
                    # and df['STOCHRSIk'].iloc[i] > df['STOCHRSIk'].iloc[i-1]:
                buy.append(i)

    desc = f'[전략11] SuperT 지표이용,  SUPERTl(1)구간일때 종가가 `{l_line}`을 우상향 SUPERs(-1)구간일때 Superts 가 내려가다가 수평으로 바뀔때매수'

    return buy, sell, superbuy, supersell, desc
