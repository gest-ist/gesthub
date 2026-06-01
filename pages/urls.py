from __future__ import annotations

from core.fluent import localized_patterns
from django.urls import path
from django.views.generic import RedirectView, TemplateView

from . import views


def template(path: str):
    """Short-hand for `TemplateView.as_view`."""
    return TemplateView.as_view(template_name=path)


gestcon_view = template("pages/gestcon.html")


ROUTES = {
    "home": (
        views.home,
        {"pt": "", "en": ""},
    ),
    "gestcon": (
        gestcon_view,
        {"pt": "gestcon/2026", "en": "gestcon/2026"},
    ),
}

urlpatterns = [
    *localized_patterns(ROUTES),
    path("gestcon/", RedirectView.as_view(url="/pt/gestcon/2026/", permanent=False)),
    path("gestcon/2026/", RedirectView.as_view(url="/pt/gestcon/2026/", permanent=False)),
    path("pt/gestcon/", RedirectView.as_view(url="/pt/gestcon/2026/", permanent=False)),
    path("en/gestcon/", RedirectView.as_view(url="/en/gestcon/2026/", permanent=False)),
]
