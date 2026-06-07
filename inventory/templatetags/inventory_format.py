from __future__ import annotations

from django import template

register = template.Library()


@register.filter
def localized_decimal(value, language: str) -> str:
    text = str(value)
    if language == "pt":
        return text.replace(".", ",")
    return text
