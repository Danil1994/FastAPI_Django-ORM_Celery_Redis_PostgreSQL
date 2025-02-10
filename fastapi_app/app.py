import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application
from .django_config import setup_django

setup_django()

django_app = get_wsgi_application()

app = FastAPI()

if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/v2")
def read_main():
    return {"message": "Hello from FastAPI!"}


# Монтируем Django на /v1
app.mount("/v1", WSGIMiddleware(django_app))
