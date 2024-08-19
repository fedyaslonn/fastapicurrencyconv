from typing import List, Optional
from pydantic import BaseModel, validator, Field, ValidationError, model_validator, root_validator
from converter.models import Currencies
from fastapi import Request

class ConvertionRequest(BaseModel):
    from_currency: Currencies
    to_currency: Currencies
    amount: float = Field(gt=0)

    @validator('from_currency', 'to_currency')
    @classmethod
    def validate_currencies(cls, obj: Currencies):
        return obj

    @root_validator(pre=True)
    def check_currencies(cls, values):
        if values.get('from_currency') == values.get('to_currency'):
            raise ValueError("Значения from_currency и to_currency должны быть различны")
        return values



class ConverterAnswer(BaseModel):
    from_currency: Currencies
    to_currency: Currencies
    amount: float = Field(gt=0)
    converted_amount: float
    rate: float

    @validator('from_currency', 'to_currency')
    @classmethod
    def validate_currencies(cls, obj: Currencies):
        return obj

    class Config:
        from_attributes = True