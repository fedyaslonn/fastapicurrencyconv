from typing import List, Dict

import requests
from fastapi import HTTPException
from datetime import date
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError


class CurrencyService:
    def __init__(self):
        self.rates = {
            'USD': 'USD',
            'EUR': 'EUR',
            'JPY': 'JPY',
        }

    def get_rate(self, from_currency: str, to_currency: str, amount: float):
        url = f'https://v6.exchangerate-api.com/v6/375f419479127567416dd663/latest/{self.rates[from_currency]}'
        response = requests.get(url)
        data = response.json()
        if from_currency not in self.rates or to_currency not in self.rates:
            raise ValueError("Недоступная валюта")
        data["base_code"] = from_currency
        rate = data["conversion_rates"][to_currency]
        converted_amount = amount * rate
        return converted_amount, rate

