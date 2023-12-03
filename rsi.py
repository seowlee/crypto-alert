import pandas as pd
import talib as ta
import time
import asyncio
from upbit import Upbit

from telegram_alert import UpbitAlertTelegramBot

if __name__ == "__main__":
    rsi_periods = 14
    # unit = 240

    upbit = Upbit()
    bot = UpbitAlertTelegramBot()

    # 기준 차트 단위. 3 = 3분봉
    CANDLE_MIN_UNIT = 240  # 4 hours

    # 불러올 최대 거래량 갯수
    MAX_COUNT = 200
    CHAT_ID = 5072827794

    while True:
        candles = upbit.candles("KRW-BTC")
        min_candles = candles.minute(unit=CANDLE_MIN_UNIT, count=MAX_COUNT)

        df = pd.DataFrame(
            data={
                "open": [x.opening_price() for x in min_candles],
                "close": [x.trade_price() for x in min_candles],
                "high": [x.high_price() for x in min_candles],
                "low": [x.low_price() for x in min_candles],
            }
        )
        df_rsi = ta.RSI(df["close"], timeperiod=14)
        now_rsi = df_rsi[-1:].values[0]
        print(now_rsi)
        time.sleep(30)

        if now_rsi > 40:
            bot.send_msg("RSI is greater than 40!")
            # asyncio.run(bot.echo(CHAT_ID, "RSI is above 50"))


# def rsi(df, periods=14, ema=True):
#     close_delta = df["close"].diff()

#     up = close_delta.clip(lower=0)
#     down = -1 * close_delta.clip(upper=0)

#     if ema:  # Exponential Moving Average
#         ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
#         ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
#     else:  # Simple Moving Average
#         ma_up = up.rolling(window=periods).mean()
#         ma_down = down.rolling(window=periods).mean()

#     rsi = ma_up / ma_down
#     rsi = 100 - (100 / (1 + rsi))

#     return rsi


# df_rsi = rsi(df)
# print(df_rsi[-1:].values[0])
