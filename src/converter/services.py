from typing import List, Dict
import aiohttp
import requests
from fastapi import HTTPException, Depends
from datetime import date
from converter import schemas
from aiohttp import ClientSession

async def set_rate(request: schemas.ConvertionRequest = Depends()):
    try:
        async with aiohttp.ClientSession() as session:
            url = f'https://v6.exchangerate-api.com/v6/375f419479127567416dd663/latest/{request.from_currency.value}'
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=500, detail="Ошибка при получении данных о курсе валют")
                data = await response.json()
                data["base_code"] = request.from_currency.value
                rate = data["conversion_rates"][request.to_currency.value]
                converted_amount = request.amount * rate
                return converted_amount, rate
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {str(e)}")
