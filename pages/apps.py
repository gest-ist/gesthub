from __future__ import annotations

import os

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
        # In dev, runserver starts a parent file-watcher and a child server process.
        # RUN_MAIN is only set in the child, where the refresh thread should run.
        if settings.CALENDAR_ICAL_URL and (not settings.DEBUG or os.environ.get("RUN_MAIN") == "true"):
            from .calendar import start_calendar_refresh

            start_calendar_refresh()
