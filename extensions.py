import requests
import json
from config import keys


class APIException(Exception):
    pass


class Index:
    @staticmethod
    def get_index():
        r = requests.get(f'https://min-api.cryptocompare.com/data/pricemulti?fsyms=USD,EUR,JPY&tsyms=RUB')
        all_price = json.loads(r.content)
        usd, eur, jpy = all_price['USD']["RUB"], all_price['EUR']["RUB"], all_price['JPY']["RUB"]
        index = f'Курс валют:\nUSD-{usd}руб.\nEUR-{eur}руб.\nJPY-{jpy}руб.'
        return index


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
