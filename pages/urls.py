from __future__ import annotations

from core.fluent import localized_patterns
from django.views.generic import TemplateView


def template(path: str):
    """Short-hand for `TemplateView.as_view`."""
    return TemplateView.as_view(template_name=path)


ROUTES = {
    "home": (
        template("pages/home.html"),
        {"pt": "", "en": ""},
    ),
}

urlpatterns = localized_patterns(ROUTES)
