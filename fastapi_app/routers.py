from typing import Optional

from django.db import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from asgiref.sync import sync_to_async
from .models import Currency, Provider as DjangoProvider, Block as DjangoBlock
from .schemas import CurrencyCreate, Currency, ProviderCreate, Provider, BlockCreate, Block as BlockSchema

router = APIRouter()


@router.post("/register/")
async def register(username: str, password: str):
    existing_user = await sync_to_async(User.objects.filter(username=username).exists)()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        new_user = await sync_to_async(User.objects.create_user)(username=username, password=password)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Error creating user")

    return {"msg": "User registered successfully", "user_id": new_user.id}


@router.post("/login/")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    db_user = await sync_to_async(User.objects.filter(username=user.username).first)()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username")

    if not db_user.check_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    return {"msg": "Login successful", "user_id": db_user.id}


@sync_to_async
def get_blocks_from_db(currency_name: Optional[str] = None,
                       provider_name: Optional[str] = None,
                       offset: int = 0,
                       limit: int = 10):
    query = DjangoBlock.objects.all()

    if currency_name:
        query = query.filter(currency__name=currency_name)

    if provider_name:
        query = query.filter(provider__name=provider_name)

    total_count = query.count()
    blocks = list(query[offset:offset + limit])

    return {"total": total_count, "blocks": blocks}


@router.get("/blocks",)
async def get_blocks(
    currency_name: Optional[str] = Query(None, description="Currency name for filtering"),
    provider_name: Optional[str] = Query(None, description="Provider name for filtering"),
    offset: int = Query(0, ge=0, description="Offset for pagination (default: 0)"),
    limit: int = Query(10, ge=1, le=100, description="Limit per page (default: 10, max: 100)")
):
    result = await get_blocks_from_db(currency_name, provider_name, offset, limit)

    if not result["blocks"]:
        raise HTTPException(status_code=404, detail="No blocks found")

    return {
        "total": result["total"],
        "count": len(result["blocks"]),
        "offset": offset,
        "limit": limit,
        "blocks": result["blocks"],
    }


@sync_to_async
def get_block_from_db_with_id(block_id: int):
    return DjangoBlock.objects.get(id=block_id)


@router.get("/blocks/{block_id}")
async def get_block(block_id: int):
    try:
        block = await get_block_from_db_with_id(block_id)
        return block
    except DjangoBlock.DoesNotExist:
        raise HTTPException(status_code=404, detail="Block not found")


@sync_to_async
def get_block_from_db_with_cur_num(currency: str, block_number: int):
    try:
        return DjangoBlock.objects.get(currency__name=currency, block_number=block_number)
    except DjangoBlock.DoesNotExist:
        return None


@router.get("/block/{currency}/{block_number}")
async def get_block(currency: str, block_number: int):
    try:
        block = await get_block_from_db_with_cur_num(currency, block_number)
        return block
    except DjangoBlock.DoesNotExist:
        raise HTTPException(status_code=404, detail="Block not found")


@sync_to_async
def get_providers_from_db(offset: int = 0, limit: int = 10):
    query = DjangoProvider.objects.all()

    total_count = query.count()
    providers = list(query[offset:offset + limit])

    return {"total": total_count, "providers": providers}


@router.get("/providers", response_model=dict)
async def get_providers(
        offset: int = Query(0, ge=0, description="Offset for pagination (default: 0)"),
        limit: int = Query(10, ge=1, le=100, description="Limit per page (default: 10, max: 100)")
):
    result = await get_providers_from_db(offset, limit)

    if not result["providers"]:
        raise HTTPException(status_code=404, detail="No providers found")

    return {
        "total": result["total"],
        "count": len(result["providers"]),
        "offset": offset,
        "limit": limit,
        "providers": result["providers"],
    }
