from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()

class Currencies(Enum):
    USD = 'USD'
    EUR = 'EUR'
    JPY = 'JPY'

class Operation(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    from_currency = Column(Currencies, nullable=False)
    to_currency = Column(Currencies, nullable=False)
    amount = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())

    async def create_operation(session: AsyncSession, from_currency: Currencies, to_currency: Currencies, amount: int):
        operation = Operation(from_currency=from_currency,
                          to_currency=to_currency,
                          amount=amount)
        session.add(operation)
        await session.commit()
        return operation.id