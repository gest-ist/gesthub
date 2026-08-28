"""Development settings."""

from __future__ import annotations

from .base import *  # noqa: F403

DEBUG = True
SECRET_KEY = SECRET_KEY or "django-insecure-local-development-only"  # noqa: F405
ALLOWED_HOSTS = ALLOWED_HOSTS or ["localhost", "127.0.0.1", "[::1]"]  # noqa: F405
