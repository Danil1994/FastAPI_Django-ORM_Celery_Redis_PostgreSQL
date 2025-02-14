import os
from datetime import datetime

import django
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.local')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
API_KEY_BLOCKCHAIR = os.getenv("API_KEY_BLOCKCHAIR")
API_KEY_COINMARKETCAP = os.getenv("API_KEY_COINMARKETCAP")
django.setup()

from celery import shared_task
from django.utils.timezone import now

from fastapi_app.celery_config import celery_app
from fastapi_app.models import Block, Currency, Provider

COINMARKETCAP_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
BLOCKCHAIR_ETH_URL = "https://api.blockchair.com/ethereum/stats"


@shared_task
def fetch_btc_block(api_key: str):
    headers = {
        "X-CMC_PRO_API_KEY": api_key
    }
    response = requests.get(COINMARKETCAP_URL, headers=headers)
    data = response.json()

    btc_data = next((item for item in data.get("data", []) if item.get("symbol") == "BTC"), None)
    if not btc_data:
        return "BTC data not found"

    currency, _ = Currency.objects.get_or_create(name="BTC")

    provider, created = Provider.objects.get_or_create(
        name="CoinMarketCap",
    )

    if not created and provider.api_key != api_key:
        provider.api_key = api_key
        provider.save()

    block_number = btc_data["num_market_pairs"]

    date_added_str = btc_data["date_added"]
    date_added = datetime.strptime(date_added_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    date_added = date_added.replace(tzinfo=None)

    if not Block.objects.filter(block_number=block_number, currency=currency).exists():
        Block.objects.create(
            currency=currency,
            provider=provider,
            block_number=block_number,
            created_at=date_added,
        )

    return f"BTC Block {block_number} saved"


@shared_task
def fetch_eth_block(api_key: str):
    headers = {"X-API-Key": api_key} if api_key else {}
    response = requests.get(BLOCKCHAIR_ETH_URL, headers)
    data = response.json()

    if "data" not in data or not data["data"]:
        return "No ETH data found"

    latest_block = data["data"]
    block_number = latest_block["blocks"]

    currency, _ = Currency.objects.get_or_create(name="ETH")

    provider, created = Provider.objects.get_or_create(
        name="BlockChair",
        defaults={"api_key": api_key}
    )

    if not created and provider.api_key != api_key:
        provider.api_key = api_key
        provider.save()

    if not Block.objects.filter(block_number=block_number, currency=currency).exists():
        Block.objects.create(
            currency=currency,
            provider=provider,
            block_number=block_number,
            created_at=now(),
        )

    return f"ETH Block {block_number} saved"


# if __name__ == '__main__':
#     fetch_btc_block(API_KEY_COINMARKETCAP)
#     fetch_eth_block(API_KEY_BLOCKCHAIR)
