from __future__ import annotations

from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path(_("contact/"), views.contact, name="contact"),
]
