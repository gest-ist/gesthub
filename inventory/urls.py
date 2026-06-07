from __future__ import annotations

from core.fluent import localized_patterns

from . import views


ROUTES = {
    "collection": (
        views.collection,
        {"pt": "ludoteca", "en": "library"},
    ),
}


urlpatterns = [
    *localized_patterns(ROUTES),
]
