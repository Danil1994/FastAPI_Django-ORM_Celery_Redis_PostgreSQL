from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ReadUserSchema(BaseModel):
    uuid: UUID
    username: str
    email: str

    class Config:
        orm_mode = True


class CreateUserSchema(BaseModel):
    username: str
    email: str
    password: str


class CurrencyBase(BaseModel):
    name: str


class CurrencyCreate(CurrencyBase):
    pass


class Currency(CurrencyBase):
    id: int

    class Config:
        orm_mode = True


class ProviderBase(BaseModel):
    name: str
    api_key: str


class ProviderCreate(ProviderBase):
    pass


class Provider(ProviderBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

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
