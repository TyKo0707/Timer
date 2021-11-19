import aiohttp
import asyncio
import typing
import requests
from datetime import datetime
from models import *

BASE_URL = "https://testnet.binancefuture.com"
PUBLIC_KEY = 'de4dc02f2eef2d9f0c488c9ff0bcff27fedeb21ca18e4374bfb4bc15f341c74d'

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def make_request(method: str, endpoint: str, data: typing.Dict):
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
        return response.json()
    else:
        return None


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