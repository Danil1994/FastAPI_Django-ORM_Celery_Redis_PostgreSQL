import os
import django
from faker import Faker

from django.utils import timezone
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastapi_app.settings')
django.setup()

from fastapi_app.models import Currency, Provider, Block

fake = Faker()


def create_fake_data(blocks_num=10, currenies_num=5):
    currencies = []

    for _ in range(currenies_num):
        currency = Currency.objects.create(name=fake.lexify(text="???").upper())
        currencies.append(currency)
    providers = []

    for _ in range(3):
        provider = Provider.objects.create(
            name=fake.company(),
            api_key=fake.uuid4()
        )
        providers.append(provider)

    for _ in range(blocks_num):
        block = Block.objects.create(
            currency=random.choice(currencies),
            provider=random.choice(providers),
            block_number=random.randint(1, 10000),
            created_at=fake.date_time_this_decade(),
            stored_at=timezone.now()
        )
    print(f"Created block {block.block_number} for currency {block.currency.name}")


create_fake_data()

if __name__ == "__main__":
    create_fake_data()
