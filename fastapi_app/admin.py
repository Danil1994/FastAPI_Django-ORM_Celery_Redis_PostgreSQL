from django.contrib import admin

from fastapi_app.models import Block, Currency, Provider


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "api_key")
    search_fields = ("name",)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("id", "block_number", "created_at", "stored_at", "currency_id", "provider_id")
    search_fields = ("name",)
