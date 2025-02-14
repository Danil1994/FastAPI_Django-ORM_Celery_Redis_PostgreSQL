import os

from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

from config.settings import setup_django

from .routers import router as fastapi_router

setup_django()

django_app = get_wsgi_application()

app = FastAPI()

if not os.path.exists("../static"):
    os.makedirs("../static")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/django", WSGIMiddleware(django_app))
app.include_router(fastapi_router)


@app.get("/")
def read_main():
    return {"message": "Hello from FastAPI!"}
