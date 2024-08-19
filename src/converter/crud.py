from . import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
# from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends
from users.crud import get_current_user

async def get_last_operations(session: AsyncSession, user_id: int):
    try:
        query = (
            select(models.Operation)
            .where(models.Operation.user_id == user_id)
            .order_by(desc(models.Operation.created_at))
            .limit(10)
        )
        result = await session.execute(query)
        last_operations = result.scalars().all()
        return last_operations
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка при обращении к базе данных.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка: " + str(e))

async def get_last_operation(session: AsyncSession, user_id: int):
    try:
        query = (
            select(models.Operation)
            .where(models.Operation.user_id == user_id)
            .order_by(desc(models.Operation.created_at))
        )
        result = await session.execute(query)
        last_operation = result.scalars().first()
        return last_operation
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка при обращении к базе данных.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка: " + str(e))
async def get_operations(session: AsyncSession, user_id: int):
    try:
        query = (
        select(models.Operation)
        .where(models.Operation.user_id == user_id)
        )
        result = await session.execute(query)
        operations = result.scalars().all()
        return operations
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка при обращении к базе данных.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка: " + str(e))

async def create_operation(session: AsyncSession, answer: schemas.ConverterAnswer, user_id: int):
    try:
        operation = models.Operation(
            from_currency=answer.from_currency,
            to_currency=answer.to_currency,
            amount=answer.amount,
            converted_amount=answer.converted_amount,
            rate=answer.rate,
            user_id=user_id
        )
        session.add(operation)
        await session.commit()
        await session.refresh(operation)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка: " + str(e))
