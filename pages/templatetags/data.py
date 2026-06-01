from __future__ import annotations

from collections.abc import Mapping

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def get_item(value: Mapping[str, str], key: str) -> str:
    return value.get(key) or value.get(settings.LANGUAGE_CODE) or ""
