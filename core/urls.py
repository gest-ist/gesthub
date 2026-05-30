"""Root URL configuration for the GEST site."""

from __future__ import annotations

from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/pt/", permanent=False)),
    path("", include("pages.urls")),
]
