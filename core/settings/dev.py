"""Development settings."""

from __future__ import annotations

from .base import *  # noqa: F403

DEBUG = True
SECRET_KEY = SECRET_KEY or "django-insecure-local-development-only"  # noqa: F405

LOCALHOST_HOSTS = ["localhost", "127.0.0.1", "[::1]"]
ALLOWED_HOSTS = list(dict.fromkeys((ALLOWED_HOSTS or []) + LOCALHOST_HOSTS))  # noqa: F405
