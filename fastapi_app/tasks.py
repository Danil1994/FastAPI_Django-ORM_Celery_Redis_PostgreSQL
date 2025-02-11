from datetime import datetime

import requests
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastapi_app.settings')
django.setup()
# from celery import shared_task
from django.utils.timezone import now
from fastapi_app.models import Block, Currency, Provider

COINMARKETCAP_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
BLOCKCHAIR_ETH_URL = "https://api.blockchair.com/ethereum/stats"

HEADERS = {"X-CMC_PRO_API_KEY": "9c8d92e2-9a34-4d4a-8a53-0280eca1e7d3"}

#
# @shared_task
def fetch_btc_block():
    """Получает последний блок BTC из CoinMarketCap и сохраняет его"""
    response = requests.get(COINMARKETCAP_URL, headers=HEADERS)
    data = response.json()

    btc_data = next((item for item in data["data"] if item["symbol"] == "BTC"), None)
    if not btc_data:
        return "BTC data not found"

    for _ in btc_data:
        print(_, btc_data[_])

    currency, _ = Currency.objects.get_or_create(name="BTC")
    provider, _ = Provider.objects.get_or_create(name="CoinMarketCap")

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


# @shared_task
def fetch_eth_block():
    """Получает последний блок ETH из BlockChair и сохраняет его"""
    response = requests.get(BLOCKCHAIR_ETH_URL)
    data = response.json()
    print(f"From blockchain data: {data}")

    if "data" not in data or not data["data"]:
        return "No ETH data found"

    latest_block = data["data"]
    block_number = latest_block["blocks"]

    currency, _ = Currency.objects.get_or_create(name="ETH")
    provider, _ = Provider.objects.get_or_create(name="BlockChair")

    if not Block.objects.filter(block_number=block_number, currency=currency).exists():
        Block.objects.create(
            currency=currency,
            provider=provider,
            block_number=block_number,
            created_at=now(),
        )

    return f"ETH Block {block_number} saved"


if __name__ == '__main__':
    fetch_btc_block()
