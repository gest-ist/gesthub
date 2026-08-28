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

"""How to add a partner:

1. Put the partner logo in static/partners_logos/. Keep the filename and case
    consistent with the file on disk.
2. Add an entry to PARTNERS below. Set:
    - logo: the path relative to static/, for example
      "partners_logos/example.png".
    - name: the partner's name as written by the partner.
    - thanks_key: a unique Fluent key, for example
      "partner-example-thanks".
    - url: the partner's website, including https://.
3. Add the thanks_key to all locale files:
    - locales/pt/pages.ftl
    - locales/en/pages.ftl
    - locales/es/pages.ftl
    Translate the thank-you message separately in each file.
4. Do not edit partners.html for each new partner. The template already
    renders the logo link, name, and translated thank-you message.
5. Run `python manage.py check` and visit each language URL to verify the
    logo, external link, and translations.

Example entry:
     {
          "logo": "partners_logos/example.png",
          "name": "Example Partner",
          "thanks_key": "partner-example-thanks",
          "url": "https://example.com/",
     },
"""

PARTNERS = [
    {
        "logo": "partners_logos/jogomesa_vectorial.svg",
        "name": "Jogo na Mesa",
        "thanks_key": "partner-jogonamesa-thanks",
        "url": "https://jogonamesa.pt/",
        "gestcon_link": True,
    },
    {
        "logo": "partners_logos/newborn_games.png",
        "name": "Newborn Games",
        "thanks_key": "partner-newborn-games-thanks",
        "url": "https://newborngames.pt/",
    },
    {
        "logo": "partners_logos/gamesomnivorous.jpg",
        "name": "Games Omnivorous",
        "thanks_key": "partner-games-omnivorous-thanks",
        "url": "https://gamesomnivorous.com/",
    },
    {
        "logo": "partners_logos/aeist.svg",
        "name": "AEIST",
        "thanks_key": "partner-aeist-thanks",
        "url": "https://aeist.pt/",
    },
    {
        "logo": "partners_logos/Galp_Logo_Standard.png",
        "name": "Galp",
        "thanks_key": "partner-galp-thanks",
        "url": "https://galp.com/",
    },
    {
        "logo": "partners_logos/logo-santander.svg",
        "name": "Santander",
        "thanks_key": "partner-santander-thanks",
        "url": "https://santander.pt/",
    },
]

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


def partners(request):
    return render(
        request,
        "pages/partners.html",
        {
            "partners": PARTNERS,
            "gestcon_url": request.path.replace("parceiros", "gestcon/2026"),
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
