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
                and df['SMA5'].iloc[i - 2] < df['SMA5'].iloc[i-3]:
            # and df['RSI'].iloc[i] < df['RSI'].iloc[i-1] \
            # and df['MFI'].iloc[i] < df['MFI'].iloc[i-1]:


            sell.append(i)
            # if trigger == True:
            #     sell.append(i)
            #     trigger = False

        if df.SUPERTs[i-1] > df.Close.iloc[i-1] and df.SUPERTl[i] < df.Close.iloc[i]:
            superbuy.append(i)
        elif df.SUPERTl[i-1] < df.Close.iloc[i-1] and df.SUPERTs[i] > df.Close.iloc[i]:
            supersell.append(i)

    return buy, sell, superbuy, supersell


# # -----------------------------   전략 2 ---------------------------------------
# # RSI 지표가 50을 돌파 할때 매수 50을 하락 할때 매도
# def strategy02(df):
#     buy, sell, superbuy, supersell = [], [], [], []
#     trigger = False
#     for i in range(2, len(df)):
#         if df.RSI.iloc[i] > 50 > df.RSI.iloc[i - 1] > df.RSI.iloc[i - 2]:
#             if trigger == False:
#                 buy.append(i)
#                 trigger = True
#         elif df.RSI.iloc[i] < 50 < df.RSI.iloc[i - 1] < df.RSI.iloc[i - 2]:
#             if trigger == True:
#                 sell.append(i)
#                 trigger = False
#
#         if df.SUPERTs[i-1] > df.close.iloc[i-1] and df.SUPERTl[i] < df.close.iloc[i]:
#             superbuy.append(i)
#         elif df.SUPERTl[i-1] < df.close.iloc[i-1] and df.SUPERTs[i] > df.close.iloc[i]:
#             supersell.append(i)
#
#     return buy, sell, superbuy, supersell
#
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
        if df.SUPERTs[i-1] > df.Close.iloc[i-1] and df.SUPERTl[i] < df.Close.iloc[i]:
            superbuy.append(i)
        elif df.SUPERTl[i-1] < df.Close.iloc[i-1] and df.SUPERTs[i] > df.Close.iloc[i]:
            supersell.append(i)

    return buy, sell, superbuy, supersell


# # -----------------------------   전략 4 ---------------------------------------
# # # 5 이평선이 20 이평선 아래에서 V 자 반등 할때
# # def strategy04(df):
# #     buy, sell = [], []
# #     for i in range(2, len(df)):
# #         if df.MA20.iloc[i] > df.MA5.iloc[i] > df.MA5.iloc[i-1] \
# #                 and df.MA5.iloc[i-1] <= df.MA5.iloc[i-2] \
# #                 and df.MA5.iloc[i-2] < df.MA5.iloc[i-3]:
# #             buy.append(i)
# #         elif df.MA20.iloc[i] < df.MA5.iloc[i] < df.MA5.iloc[i-1] \
# #                 and df.MA5.iloc[i-1] >= df.MA5.iloc[i-2] \
# #                 and df.MA5.iloc[i-2] > df.MA5.iloc[i-3]:
# #             sell.append(i)
# #
# #     return buy, sell
# #
# #
#
# # -----------------------------   전략 5 ---------------------------------------
# # # 5 이평선이 20 이평선 아래에서 V 자 반등 할때 rsi가 지정수 이상 일때
# # def strategy05(df):
# #     buy, sell = [], []
# #     for i in range(2, len(df)):
# #         if df.MA20.iloc[i] > df.MA5.iloc[i] > df.MA5.iloc[i-1] \
# #                 and df.MA5.iloc[i-1] <= df.MA5.iloc[i-2] \
# #                 and df.MA5.iloc[i-2] < df.MA5.iloc[i-3]\
# #                 and df.rsi.iloc[i] > df.rsi.iloc[i-1] > 30:
# #             buy.append(i)
# #         elif df.MA20.iloc[i] < df.MA5.iloc[i] < df.MA5.iloc[i-1] \
# #                 and df.MA5.iloc[i-1] >= df.MA5.iloc[i-2] \
# #                 and df.MA5.iloc[i-2] > df.MA5.iloc[i-3]:
# #             sell.append(i)
# #
# #     return buy, sell
#
# # -----------------------------   전략 6 ---------------------------------------
# # mfi 가 50이상에서 macd가 골든 크로스 할때
# def strategy06(df):
#     buy, sell, superbuy, supersell = [], [], [], []
#     trigger = False
#     for i in range(2, len(df)):
#         if df.MFI.iloc[i] > df.MFI.iloc[i-1] > 50 \
#                 and df.MACD.iloc[i] > df.MACD.iloc[i-1] \
#                 and df.MACD.iloc[i] > df.MACDs.iloc[i] \
#                 and df.MACD.iloc[i-1] < df.MACDs.iloc[i-1]:
#             if trigger == False:
#                 buy.append(i)
#                 trigger = True
#         elif df.MFI.iloc[i-1] > df.MFI.iloc[i] \
#                 and df.MACD.iloc[i] < df.MACD.iloc[i-1] \
#                 and df.MACD.iloc[i] < df.MACDs.iloc[i] \
#                 and df.MACD.iloc[i-1] > df.MACDs.iloc[i-1]:
#             if trigger == True:
#                 sell.append(i)
#                 trigger = False
#
#     return buy, sell, superbuy, supersell

# -----------------------------   전략 7 ---------------------------------------
# trix가 0을 돌파할때
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
        if df.SUPERTs[i-1] > df.Close.iloc[i-1] and df.SUPERTl[i] < df.Close.iloc[i]:
            superbuy.append(i)
        elif df.SUPERTl[i-1] < df.Close.iloc[i-1] and df.SUPERTs[i] > df.Close.iloc[i]:
            supersell.append(i)

    return buy, sell, superbuy, supersell

# -----------------------------   전략 8 ---------------------------------------
# trix가 TRIXs 을 돌파할때---------------- (0 이상 0이하 로 시도 해볼것.,)
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
        if df.SUPERTs[i-1] > df.Close.iloc[i-1] and df.SUPERTl[i] < df.Close.iloc[i]:
            superbuy.append(i)
        elif df.SUPERTl[i-1] < df.Close.iloc[i-1] and df.SUPERTs[i] > df.Close.iloc[i]:
            supersell.append(i)

    return buy, sell, superbuy, supersell