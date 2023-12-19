import asyncio
from telegram_alert import UpbitAlertTelegramBot
from upbit import Upbit
import pandas as pd
import talib as ta
import sys
import time
import asyncio
from upbit import Upbit

if __name__ == "__main__":
    # Create an instance of the UpbitAlertTelegramBot class
    bot = UpbitAlertTelegramBot()

    upbit = Upbit()

    # 기준 차트 단위. 3 = 3분봉
    CANDLE_MIN_UNIT = 240  # 4 hours

    # 불러올 최대 거래량 갯수
    MAX_COUNT = 200
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
        time.sleep(10)
        msg = "RSI is greater than 40!"
        if now_rsi > 40:
            message = " ".join(sys.argv[1:]) or "RSI is greater than 40!"
            # asyncio.set_event_loop_policy(asyncio.set_event_loop_policy())
            asyncio.run(bot.send_alert(message), debug=False)

        time.sleep(30)
