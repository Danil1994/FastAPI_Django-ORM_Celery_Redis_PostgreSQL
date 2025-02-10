from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application
from .django_config import setup_django

setup_django()  # Настроим Django

django_app = get_wsgi_application()  # Получаем WSGI-приложение Django

app = FastAPI()


@app.get("/v2")
def read_main():
    return {"message": "Hello from FastAPI!"}


# Монтируем Django на /v1
app.mount("/v1", WSGIMiddleware(django_app))
