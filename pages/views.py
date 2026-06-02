from __future__ import annotations

from hashlib import blake2s
from urllib.parse import urlparse

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_sameorigin

from .calendar import get_calendar, month_context
from .gallery import load_gallery


CALENDAR_ORIGIN_URL = settings.CALENDAR_ORIGIN_URL if urlparse(settings.CALENDAR_ORIGIN_URL).netloc else ""
CALENDAR_ORIGIN_HASH = blake2s(CALENDAR_ORIGIN_URL.encode(), digest_size=8).hexdigest()


def home(request):
    return render(
        request,
        "pages/home.html",
        {
            "home_gallery": load_gallery("home"),
        },
    )


def gestcon_gallery(request):
    return render(
        request,
        "pages/gestcon_gallery.html",
        {
            "gallery": load_gallery("gestcon/2026"),
        },
    )


@xframe_options_sameorigin
def calendar_embed(request):
    today = timezone.localdate()
    year = int(request.GET.get("year") or today.year)
    month = int(request.GET.get("month") or today.month)
    if month < 1 or month > 12:
        month = today.month

    state = get_calendar()
    if state is None:
        return render(
            request,
            "pages/calendar_embed.html",
            {
                **month_context(year, month, state),
                "calendar_origin_url": CALENDAR_ORIGIN_URL,
            },
        )

    loaded_at = state.loaded_at.isoformat()
    cache_key = f"calendar-embed:{request.LANGUAGE_CODE}:{year}:{month}:{loaded_at}:{CALENDAR_ORIGIN_HASH}"
    cached_html = cache.get(cache_key)
    if cached_html is not None:
        return HttpResponse(cached_html)

    html = render_to_string(
        "pages/calendar_embed.html",
        {
            **month_context(year, month, state),
            "calendar_origin_url": CALENDAR_ORIGIN_URL,
        },
        request=request,
    )
    cache.set(cache_key, html, timeout=None)
    return HttpResponse(html)
