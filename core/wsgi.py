"""WSGI config for the GEST site."""

from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.prod")

application = get_wsgi_application()
