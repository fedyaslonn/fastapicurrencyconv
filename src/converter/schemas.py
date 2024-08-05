from typing import Optional, List
from pydantic import BaseModel, validator, Field, ValidationError


class ConvertionRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float = Field(gt=0)

    @validator('from_currency', 'to_currency')
    @classmethod
    def validate_currencies(cls, obj):
        currency_list = ['JPY', 'PHP', 'SEK', 'EUR', 'NOK', 'ILS', 'THB', 'ISK', 'MXN', 'CAD', 'MTL', 'CNY', 'HUF',
                         'KRW',
                         'IDR', 'GBP', 'EEK', 'INR', 'NZD', 'TRL', 'PLN', 'CYP', 'LVL', 'BRL', 'HKD', 'AUD', 'MYR',
                         'ROL', 'CHF', 'CZK', 'HRK',
                         'SKK', 'SIT', 'TRY', 'USD', 'RON', 'SGD', 'ZAR', 'BGN', 'RUB', 'DKK']
        if obj not in currency_list:
            raise ValueError(f"Неправильный ввод курса: {obj}")
        return obj


class ConverterAnswer(BaseModel):
    from_currency: str
    to_currency: str
    amount: float = Field(gt=0)
    converted_amount: float
    rate: float

    @validator('from_currency', 'to_currency')
    @classmethod
    def validate_currencies(cls, obj):
        currency_list = ['JPY', 'PHP', 'SEK', 'EUR', 'NOK', 'ILS', 'THB', 'ISK', 'MXN', 'CAD', 'MTL', 'CNY', 'HUF',
                         'KRW',
                         'IDR', 'GBP', 'EEK', 'INR', 'NZD', 'TRL', 'PLN', 'CYP', 'LVL', 'BRL', 'HKD', 'AUD', 'MYR',
                         'ROL', 'CHF', 'CZK', 'HRK',
                         'SKK', 'SIT', 'TRY', 'USD', 'RON', 'SGD', 'ZAR', 'BGN', 'RUB', 'DKK']
        if obj not in currency_list:
            raise ValueError(f"Неправильный ввод курса: {obj}")
        return obj