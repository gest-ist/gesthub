from __future__ import annotations

from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"  # we don't need 64 bit IDs
    name = "inventory"
    verbose_name = "Inventory"
