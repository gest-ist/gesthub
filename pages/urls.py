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
        {"pt": "", "en": "", "es": ""},
    ),
    "gestcon": (
        gestcon_view,
        {"pt": "gestcon/2026", "en": "gestcon/2026", "es": "gestcon/2026"},
    ),
    "gestcon_gallery": (
        views.gestcon_gallery,
        {"pt": "gestcon/2026/galeria", "en": "gestcon/2026/gallery", "es": "gestcon/2026/galeria"},
    ),
    "partners": (
        views.partners,
        {"pt": "parceiros", "en": "parceiros", "es": "parceiros"},
    ),
}

urlpatterns = [
    path("calendar/embed/", views.calendar_embed, name="calendar_embed"),
    path("pt/calendar/embed/", views.calendar_embed, name="pt-calendar_embed"),
    path("en/calendar/embed/", views.calendar_embed, name="en-calendar_embed"),
    path("es/calendar/embed/", views.calendar_embed, name="es-calendar_embed"),
    *localized_patterns(ROUTES),
    path("parceiros/", RedirectView.as_view(url="/pt/parceiros/", permanent=False)),
    path("gestcon/", RedirectView.as_view(url="/pt/gestcon/2026/", permanent=False)),
    path("gestcon/2026/", RedirectView.as_view(url="/pt/gestcon/2026/", permanent=False)),
    path("pt/gestcon/", RedirectView.as_view(url="/pt/gestcon/2026/", permanent=False)),
    path("en/gestcon/", RedirectView.as_view(url="/en/gestcon/2026/", permanent=False)),
]
