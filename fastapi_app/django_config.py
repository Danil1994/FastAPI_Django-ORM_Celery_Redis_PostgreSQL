import os
import django
from django.conf import settings

def setup_django():
    if not settings.configured:
        settings.configure(
            SECRET_KEY='django-insecure-(vm=(p256-p=7urt1$r_a#$p-c6c0++2b(t7c9w7dz(1!4mcqz',
            INSTALLED_APPS=[
                "django.contrib.admin",
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "django.contrib.messages",
                "django.contrib.staticfiles",
            ],
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": "db.sqlite3",
                }
            },
            MIDDLEWARE=[
                "django.middleware.security.SecurityMiddleware",
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
            ],
            ROOT_URLCONF="fastapi_app.urls",
            DEBUG=True,
        )
        django.setup()


setup_django()
