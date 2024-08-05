from fastapi import APIRouter, Depends
from .schemas import *
from .services import *
import ssl
from .celery_app import convert_currency

converter_router = APIRouter()

@converter_router.get('/get_convert_result/', response_model=ConverterAnswer)
async def get_rate(currency_request: ConvertionRequest = Depends()):
    try:
        converted_amount, rate = CurrencyService().get_rate(
            from_currency=currency_request.from_currency, to_currency=currency_request.to_currency,
            amount=currency_request.amount
        )
        convert_currency.delay(from_currency=currency_request.from_currency, to_currency=currency_request.to_currency,
            amount=currency_request.amount)
        return ConverterAnswer(from_currency=currency_request.from_currency,
                               to_currency=currency_request.to_currency,
                               amount=currency_request.amount,
                               converted_amount=converted_amount,
                               rate=rate)
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))