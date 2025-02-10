from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CurrencyBase(BaseModel):
    name: str


class CurrencyCreate(CurrencyBase):
    pass


class Currency(CurrencyBase):
    id: int

    class Config:
        orm_mode = True  # Это нужно, чтобы Pydantic мог работать с ORM моделями Django


class ProviderBase(BaseModel):
    name: str
    api_key: str


class ProviderCreate(ProviderBase):
    pass


class Provider(ProviderBase):
    id: int

    class Config:
        orm_mode = True


class BlockBase(BaseModel):
    block_number: int
    created_at: Optional[datetime] = None
    stored_at: datetime


class BlockCreate(BlockBase):
    currency_id: int
    provider_id: int


class Block(BlockBase):
    id: int
    currency: Currency
    provider: Provider

    class Config:
        orm_mode = True
