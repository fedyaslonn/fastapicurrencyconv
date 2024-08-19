from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from datetime import datetime
from pydantic import Field
from sqlalchemy_utils import ChoiceType
from enum import Enum
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from database import Base

if TYPE_CHECKING:
    from users.models import User
class Currencies(str, Enum):
    JPY = 'JPY'
    PHP = 'PHP'
    SEK = 'SEK'
    EUR = 'EUR'
    NOK = 'NOK'
    ILS = 'ILS'
    THB = 'THB'
    ISK = 'ISK'
    MXN = 'MXN'
    CAD = 'CAD'
    MTL = 'MTL'
    CNY = 'CNY'
    HUF = 'HUF'
    KRW = 'KRW'
    IDR = 'IDR'
    GBP = 'GBP'
    EEK = 'EEK'
    INR = 'INR'
    NZD = 'NZD'
    TRL = 'TRL'
    PLN = 'PLN'
    CYP = 'CYP'
    LVL = 'LVL'
    BRL = 'BRL'
    HKD = 'HKD'
    AUD = 'AUD'
    MYR = 'MYR'
    ROL = 'ROL'
    CHF = 'CHF'
    CZK = 'CZK'
    HRK = 'HRK'
    SKK = 'SKK'
    SIT = 'SIT'
    TRY = 'TRY'
    USD = 'USD'
    RON = 'RON'
    SGD = 'SGD'
    ZAR = 'ZAR'
    BGN = 'BGN'
    RUB = 'RUB'
    DKK = 'DKK'

currency_choices = [(currency.name, currency.value) for currency in Currencies.__members__.values()]

class Operation(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    from_currency = Column(ChoiceType(Currencies, impl=String(3)), nullable=False)
    to_currency = Column(ChoiceType(Currencies, impl=String(3)), nullable=False)
    amount = Column(Float)
    converted_amount = Column(Float)
    rate = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="operations", lazy="joined")
