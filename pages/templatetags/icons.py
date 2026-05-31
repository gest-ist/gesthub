from __future__ import annotations

from urllib.parse import quote, urlencode

from django import template

register = template.Library()

DEFAULT_ICON_COLOR = "1d1717"
DEFAULT_ICON_SIZE = 20


def normalize_color(color: str) -> str:
    return color.removeprefix("#")


@register.simple_tag
def simple_icon(slug: str, color: str = DEFAULT_ICON_COLOR, size: int = DEFAULT_ICON_SIZE) -> str:
    """Return a Simple Icons CDN URL from icons.ly."""
    path = quote(slug.strip("/"))
    query = urlencode({"viewbox": "auto", "size": size})
    return f"https://icons.ly/{path}/{normalize_color(color)}?{query}"


@register.simple_tag
def lucide_icon(
    slug: str,
    color: str = DEFAULT_ICON_COLOR,
    size: int = DEFAULT_ICON_SIZE,
) -> str:
    """Return a Lucide icon URL from the Iconify SVG API."""
    path = quote(slug.strip("/"))
    query = urlencode(
        {
            "color": f"#{normalize_color(color)}",
            "width": size,
            "height": size,
        }
    )
    return f"https://api.iconify.design/lucide/{path}.svg?{query}"
