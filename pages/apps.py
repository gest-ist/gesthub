from __future__ import annotations

from django.conf import settings
from django.apps import AppConfig
from django.utils.autoreload import autoreload_started


def watch_fluent_files(sender, **kwargs):
    sender.watch_dir(settings.BASE_DIR / "locales", "**/*.ftl")


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"
    verbose_name = "Pages"

    def ready(self):
        autoreload_started.connect(watch_fluent_files, dispatch_uid="pages.watch_fluent_files")
