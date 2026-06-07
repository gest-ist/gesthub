from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from django.conf import settings
from django.db.models import Prefetch
from django.shortcuts import render

from .models import BoardGame, Item, ItemCopy, Lease, TtrpgAsset


@dataclass(frozen=True)
class CollectionEntry:
    item: Item
    available: bool
    ceded_to_gest: bool
    thumbnail_url: str
    image_url: str


def media_url(ref: str) -> str:
    if not ref:
        return ""

    parsed = urlparse(ref)
    if parsed.scheme or ref.startswith("/"):
        return ref

    return f"{settings.MEDIA_URL}{ref.lstrip('/')}"


def collection_entry(item: Item) -> CollectionEntry:
    visible_copies = list(item.copies.all())
    available_copies = [copy for copy in visible_copies if not copy.leases.all()]
    available = bool(available_copies)
    image_url = media_url(item.image_ref)
    return CollectionEntry(
        item=item,
        available=available,
        ceded_to_gest=available and any(not copy.is_owned_by_gest for copy in available_copies),
        thumbnail_url=media_url(item.thumbnail_ref) or image_url,
        image_url=image_url,
    )


def public_items(queryset):
    active_leases = Lease.objects.filter(return_time__isnull=True)
    visible_copies = ItemCopy.objects.filter(hidden=False).prefetch_related(
        Prefetch("leases", queryset=active_leases)
    )
    return (
        queryset.filter(copies__hidden=False)
        .distinct()
        .prefetch_related("tags", Prefetch("copies", queryset=visible_copies))
        .order_by("name")
    )


def collection(request):
    boardgames = [collection_entry(item) for item in public_items(BoardGame.objects.all())]
    ttrpg_assets = [collection_entry(item) for item in public_items(TtrpgAsset.objects.all())]

    return render(
        request,
        "inventory/collection.html",
        {
            "boardgames": boardgames,
            "ttrpg_assets": ttrpg_assets,
            "boardgame_count": len(boardgames),
            "ttrpg_count": len(ttrpg_assets),
            "unavailable_boardgame_count": sum(not entry.available for entry in boardgames),
            "unavailable_ttrpg_count": sum(not entry.available for entry in ttrpg_assets),
        },
    )
