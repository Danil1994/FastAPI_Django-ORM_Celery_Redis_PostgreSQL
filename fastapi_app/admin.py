from django.contrib import admin
from fastapi_app.models import Currency, Provider


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "api_key")
    search_fields = ("name",)
