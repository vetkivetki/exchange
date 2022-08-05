import requests
import json

from config import exchanges

class ApiException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base_key, sum_key, amount):
        base_key = base_key.upper()
        sum_key = sum_key.upper()
        try:
            base_key = exchanges[base_key.lower()]
        except KeyError:
            raise ApiException(f"Валюта {base_key} не найдена")
        try:
            sum_key = exchanges[sum_key.lower()]
        except KeyError:
            raise ApiException(f"Валюта {sum_key} не найдена")



        if base_key == sum_key:
            raise ApiException("Невозможно перевести одинаковую валюту")

        try:
            amount = float(amount)
        except ValueError:
            raise ApiException(f"Неправильная сумма")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={sum_key}')
        resp = json.loads(r.content)
        rate = resp.get(sum_key)
        new_price = rate * float(amount)
        return round(new_price, 2)
