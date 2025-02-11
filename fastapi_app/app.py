import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application
from fastapi_app.settings import setup_django
from .routers import router as fastapi_router

# os.environ['DJANGO_SETTINGS_MODULE'] = 'fastapi_app.settings'

setup_django()

django_app = get_wsgi_application()

app = FastAPI()

if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Монтируем Django на /v1
app.mount("/v1", WSGIMiddleware(django_app))
app.include_router(fastapi_router)


@app.get("/v2")
def read_main():
    return {"message": "Hello from FastAPI!"}
