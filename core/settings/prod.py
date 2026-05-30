"""Production settings."""

from __future__ import annotations

from .base import *  # noqa: F403

DEBUG = False

if not SECRET_KEY:  # noqa: F405
    msg = "DJANGO_SECRET_KEY must be set in production"
    raise RuntimeError(msg)

if not ALLOWED_HOSTS:  # noqa: F405
    msg = "DJANGO_ALLOWED_HOSTS must be set in production"
    raise RuntimeError(msg)

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")  # noqa: F405
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
