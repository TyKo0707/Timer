import aiohttp
import asyncio
import typing
import requests
from datetime import datetime

BASE_URL = "https://testnet.binancefuture.com"
PUBLIC_KEY = 'de4dc02f2eef2d9f0c488c9ff0bcff27fedeb21ca18e4374bfb4bc15f341c74d'

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class Candle:
    def __init__(self, candle_info, timeframe, exchange):
        if exchange in ["binance_futures", "binance_spot"]:
            self.timestamp = candle_info[0]
            self.open = float(candle_info[1])
            self.high = float(candle_info[2])
            self.low = float(candle_info[3])
            self.close = float(candle_info[4])
            self.volume = float(candle_info[5])


async def _make_request(method: str, endpoint: str, data: typing.Dict):
    async with aiohttp.ClientSession() as session:
        if method == "GET":
            try:
                async with session.get(BASE_URL + endpoint, params=data, headers={'X-MBX-APIKEY': PUBLIC_KEY}) as resp:
                    response = resp
                    resp_json = await resp.json()
            except Exception as e:  # Takes into account any possible error, most likely network errors
                return None

        elif method == "POST":
            try:
                async with session.post(BASE_URL + endpoint, params=data, headers={'X-MBX-APIKEY': PUBLIC_KEY}) as resp:
                    response = resp
                    resp_json = await resp.json()
            except Exception as e:
                return None

        elif method == "DELETE":
            try:
                async with session.delete(BASE_URL + endpoint, params=data,
                                          headers={'X-MBX-APIKEY': PUBLIC_KEY}) as resp:
                    response = resp
                    resp_json = await resp.json()
            except Exception as e:
                return None
        else:
            raise ValueError()

        if response.status == 200:  # 200 is the response code of successful requests
            return resp_json
        else:
            return None


def make_request(method: str, endpoint: str, data: typing.Dict):
    return loop.run_until_complete(_make_request(method, endpoint, data))


def get_historical_candles(interval: str) -> typing.List[Candle]:
    data = dict()
    data['symbol'] = 'BTCUSDT'
    data['interval'] = interval
    data['limit'] = 1000  # The maximum number of candles is 1000 on Binance Spot

    raw_candles = make_request("GET", "/fapi/v1/klines", data)

    candles = []

    if raw_candles is not None:
        for c in raw_candles:
            candles.append(Candle(c, interval, 'binance_futures'))

    # date = datetime.fromtimestamp(candles[-1].timestamp/1000)
    # return candles[-1].open, candles[-1].close, candles[-1].high, candles[-1].volume, f"{date:%Y-%m-%d %H:%M:%S}"

    return candles


def _make_request_1(method: str, endpoint: str, data: typing.Dict):
    if method == "GET":
        try:
            response = requests.get(BASE_URL + endpoint, params=data, headers={'X-MBX-APIKEY': PUBLIC_KEY})

        except Exception as e:  # Takes into account any possible error, most likely network errors
            return None

    elif method == "POST":
        try:
            response = requests.post(BASE_URL + endpoint, params=data, headers={'X-MBX-APIKEY': PUBLIC_KEY})

        except Exception as e:
            return None

    elif method == "DELETE":
        try:
            response = requests.delete(BASE_URL + endpoint, params=data, headers={'X-MBX-APIKEY': PUBLIC_KEY})

        except Exception as e:
            return None
    else:
        raise ValueError()

    if response.status_code == 200:  # 200 is the response code of successful requests
        print(response.json())
    else:
        return None


def get_historical_candles_1(interval: str) -> typing.List[Candle]:
    data = dict()
    data['symbol'] = 'BTCUSDT'
    data['interval'] = interval
    data['limit'] = 1000  # The maximum number of candles is 1000 on Binance Spot

    raw_candles = make_request("GET", "/fapi/v1/klines", data)

    candles = []

    if raw_candles is not None:
        for c in raw_candles:
            candles.append(Candle(c, interval, 'binance_futures'))



#
