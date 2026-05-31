"""Base Django settings shared by all environments."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

BASE_DIR = Path(__file__).resolve().parents[2]


def env_bool(name: str, *, default: bool = False) -> bool:
    value = os.environ.get(name)
    return value.lower() in {"1", "true", "yes", "on"} if value else default


def env_list(name: str, *, default: list[str] | None = None) -> list[str]:
    value = os.environ.get(name)
    return [item.strip() for item in value.split(",") if item.strip()] if value else default or []


def database_from_url(value: str) -> dict[str, Any]:
    parsed = urlparse(value)
    if parsed.scheme not in {"postgres", "postgresql"}:
        raise ValueError("DATABASE_URL must use postgres:// or postgresql://")

    options = {
        key: values[-1]
        for key, values in parse_qs(parsed.query, keep_blank_values=True).items()
        if values
    }

    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": unquote(parsed.path.lstrip("/")),
        "USER": unquote(parsed.username or ""),
        "PASSWORD": unquote(parsed.password or ""),
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port or ""),
        "OPTIONS": options or None,
    }


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
DEBUG = env_bool("DJANGO_DEBUG")
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django_ftl.apps.DjangoFtlConfig",
    "pages.apps.PagesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.fluent.PathLanguageMiddleware",
    "django_ftl.middleware.activate_from_request_language_code",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "core.fluent.context",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASES = {
    "default": database_from_url(DATABASE_URL)
    if DATABASE_URL
    else {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "pt"
LANGUAGES = [
    ("pt", "Português"),
    ("en", "English"),
]

TIME_ZONE = "Europe/Lisbon"
USE_I18N = False
USE_TZ = True

FTL = {
    "AUTO_RELOAD_BUNDLES": False,
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "public" / "static"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "public" / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
