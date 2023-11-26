import requests
import pandas as pd
from datetime import datetime


class Candle:
    def __init__(
        self,
        market,
        candle_date_time_utc,
        candle_date_time_kst,
        opening_price,
        high_price,
        low_price,
        trade_price,
        timestamp,
        candle_acc_trade_price,
        candle_acc_trade_volume,
        unit,
    ):
        self._market = market
        self._candle_date_time_utc = candle_date_time_utc
        self._candle_date_time_kst = candle_date_time_kst
        self._opening_price = opening_price
        self._high_price = high_price
        self._low_price = low_price
        self._trade_price = trade_price
        self._timestamp = timestamp
        self._candle_acc_trade_price = candle_acc_trade_price
        self._candle_acc_trade_volume = candle_acc_trade_volume
        self._unit = unit

    @staticmethod
    def from_json(json, unit=None):
        try:
            return Candle(
                json["market"],
                datetime.strptime(json["candle_date_time_utc"], "%Y-%m-%dT%H:%M:%S"),
                datetime.strptime(json["candle_date_time_kst"], "%Y-%m-%dT%H:%M:%S"),
                json["opening_price"],
                json["high_price"],
                json["low_price"],
                json["trade_price"],
                int(json["timestamp"]),
                json["candle_acc_trade_price"],
                json["candle_acc_trade_volume"],
                json["unit"] if unit is None else unit,
            )
        except BaseException as e:
            raise ValueError("Invalid JSON value: {}".format(json), e)

    def market(self):
        return self._market

    def candle_date_time_utc(self):
        return self._candle_date_time_utc

    def candle_date_time_kst(self):
        return self._candle_date_time_kst

    def opening_price(self):
        return self._opening_price

    def high_price(self):
        return self._high_price

    def low_price(self):
        return self._low_price

    def trade_price(self):
        return self._trade_price

    def timestamp(self):
        return self._timestamp

    def candle_acc_trade_price(self):
        return self._candle_acc_trade_price

    def candle_acc_trade_volume(self):
        return self._candle_acc_trade_volume

    def unit(self):
        return self._unit

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (
            "Candle ["
            "Market: {}, "
            "Candle Date Time UTC: {}, "
            "Candle Date Time KST: {}, "
            "Opening Price: {}, "
            "High Price: {}, "
            "Low Price: {}, "
            "Trade Price: {}, "
            "Timestamp: {}, "
            "Candle Accumulation Trade Price: {}, "
            "Candle Accumulation Trade Volume: {}, "
            "Unit: {}"
            "]".format(
                self._market,
                self._candle_date_time_utc,
                self._candle_date_time_kst,
                self._opening_price,
                self._high_price,
                self._low_price,
                self._trade_price,
                self._timestamp,
                self._candle_acc_trade_price,
                self._candle_acc_trade_volume,
                self._unit,
            )
        )


class Candles:
    def __init__(self, upbit, market):
        self._upbit = upbit
        self._market = market

    def minute(self, unit=1, count=1):
        return sorted(
            [
                Candle.from_json(x)
                for x in self._upbit._get(
                    "candles/minutes/{}".format(unit),
                    params={"market": self._market, "count": count},
                ).json()
            ],
            key=lambda x: x.candle_date_time_kst(),
        )

    def day(self, count=1, to=None):
        return sorted(
            [
                Candle.from_json(x, unit=1)
                for x in self._upbit._get(
                    "candles/days",
                    params={
                        "market": self._market,
                        "to": None if to is None else to.strftime("%Y-%m-%d %H:%M:%S"),
                        "count": count,
                    },
                ).json()
            ],
            key=lambda x: x.candle_date_time_kst(),
        )

    def week(self, count=1, to=None):
        return sorted(
            [
                Candle.from_json(x, unit=1)
                for x in self._upbit._get(
                    "candles/weeks",
                    params={
                        "market": self._market,
                        "to": None if to is None else to.strftime("%Y-%m-%d %H:%M:%S"),
                        "count": count,
                    },
                ).json()
            ],
            key=lambda x: x.candle_date_time_kst(),
        )

    def month(self, count=1, to=None):
        return sorted(
            [
                Candle.from_json(x, unit=1)
                for x in self._upbit._get(
                    "candles/months",
                    params={
                        "market": self._market,
                        "to": None if to is None else to.strftime("%Y-%m-%d %H:%M:%S"),
                        "count": count,
                    },
                ).json()
            ],
            key=lambda x: x.candle_date_time_kst(),
        )


class Upbit:
    def __init__(self):
        self._base_url = "https://api.upbit.com/v1"

    def _get(self, url, params=None):
        return requests.get(
            "{}/{}".format(self._base_url, url),
            params=params,
            headers={
                "Accept": "application/json",
            },
        )

    def candles(self, market):
        return Candles(self, market)
