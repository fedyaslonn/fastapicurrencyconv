from fastapi import APIRouter, Depends
from .schemas import *
from converter.services import set_rate
# from .celery_app import convert_currency
from typing import Optional
import aiohttp
from aiohttp import ClientSession
from database import get_session
from fastapi import HTTPException
from . import crud, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from users.crud import oauth2_scheme
from fastapi import Request
from users import crud as users_crud
from models import User
from . import crud as converter_crud

converter_router = APIRouter(tags=["Converter"])

@converter_router.get('/get_convert_result/', response_model=ConverterAnswer)
async def get_rate(currency_request: ConvertionRequest = Depends(), session: AsyncSession = Depends(get_session),
                   current_user = Depends(users_crud.get_current_user)):
    try:
        converted_amount, rate = await set_rate(currency_request)
        answer = ConverterAnswer(
            from_currency=currency_request.from_currency,
            to_currency=currency_request.to_currency,
            amount=currency_request.amount,
            converted_amount=converted_amount,
            rate=rate
        )
        create_operation = await converter_crud.create_operation(session, answer, user_id=current_user.id)
        return create_operation if create_operation else answer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@converter_router.get('/get_last_operations/')
async def get_last_operations(session: AsyncSession = Depends(get_session), current_user = Depends(users_crud.get_current_user)):
    try:
        operations_list = await converter_crud.get_last_operations(session, current_user.id)

        if not operations_list:
            raise HTTPException(status_code=404, detail="Операции не были найдены")
        return [schemas.ConverterAnswer(from_currency=operation.from_currency,
                                        to_currency=operation.to_currency,
                                        amount=operation.amount,
                                        converted_amount=operation.converted_amount,
                                        rate=operation.rate,
                                        user_id=current_user.id
                                         ) for operation in operations_list]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@converter_router.get('/get_last_operation/')
async def get_last_operation(session: AsyncSession = Depends(get_session), current_user = Depends(users_crud.get_current_user)):
    try:
        operation = await converter_crud.get_last_operation(session, current_user.id)

        if not operation:
            raise HTTPException(status_code=404, detail="Операция не была найдена")
        return [schemas.ConverterAnswer(from_currency=operation.from_currency,
                                    to_currency=operation.to_currency,
                                    amount=operation.amount,
                                    converted_amount=operation.converted_amount,
                                    rate=operation.rate)]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@converter_router.get('/get_operations/')
async def get_operations(session: AsyncSession = Depends(get_session), current_user = Depends(users_crud.get_current_user)):
    try:
        operations = await converter_crud.get_operations(session, current_user.id)

        if not operations:
            raise HTTPException(status_code=404, detail="Операции не были найдены")
        return [schemas.ConverterAnswer(from_currency=operation.from_currency,
                                    to_currency=operation.to_currency,
                                    amount=operation.amount,
                                    converted_amount=operation.converted_amount,
                                    rate=operation.rate) for operation in operations]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))