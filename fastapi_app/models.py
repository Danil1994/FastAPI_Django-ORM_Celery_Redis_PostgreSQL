from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=10, unique=True)


class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)


class Block(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    block_number = models.BigIntegerField(unique=True)
    created_at = models.DateTimeField()
    stored_at = models.DateTimeField(auto_now_add=True)
