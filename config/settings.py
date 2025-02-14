import os

import django
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # fastapi_app/
PROJECT_ROOT = os.path.dirname(BASE_DIR)


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
                'fastapi_app',
            ],
            # uncomment for SQLite using

            # DATABASES={
            #     "default": {
            #         "ENGINE": "django.db.backends.sqlite3",
            #         "NAME": os.path.join(PROJECT_ROOT, "db.sqlite3"),
            #     }
            # },

            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": os.getenv("POSTGRES_DB", "postgres"),
                    "USER": os.getenv("POSTGRES_USER", "postgres"),
                    "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
                    "HOST": os.getenv("POSTGRES_HOST", "postgres_db"),
                    "PORT": os.getenv("POSTGRES_PORT", "5432"),
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
            STATIC_URL="/static/",
            STATIC_ROOT=os.path.join(PROJECT_ROOT, "../static"),
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [],
                    "APP_DIRS": True,
                    "OPTIONS": {
                        "context_processors": [
                            "django.template.context_processors.debug",
                            "django.template.context_processors.request",
                            "django.contrib.auth.context_processors.auth",
                            "django.contrib.messages.context_processors.messages",
                        ],
                    },
                },
            ],
        )
        django.setup()


setup_django()
