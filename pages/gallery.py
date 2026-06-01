from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import nestedtext
from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GalleryItem:
    id: str
    url: str
    alts: dict[str, str]


def load_gallery(name: str) -> list[GalleryItem]:
    manifest_path = settings.MEDIA_ROOT / name / "gallery.nt"

    if not manifest_path.is_file():
        logger.warning("Gallery manifest does not exist: %s", manifest_path)
        return []

    try:
        manifest = nestedtext.load(manifest_path)
    except Exception as error:
        logger.warning("%s: %s", error.__class__.__name__, error)
        return []

    if not isinstance(manifest, dict):
        logger.warning("TypeError: gallery manifest must be a dictionary")
        return []

    items = []
    for filename, alts in manifest.items():
        try:
            item = parse_gallery_item(name, filename, alts)
        except Exception as error:
            logger.warning("%s: %s", error.__class__.__name__, error)
            continue

        if item is not None:
            items.append(item)

    return items


def parse_gallery_item(name: str, filename: str, alts: dict[str, str]) -> GalleryItem | None:
    image_path = settings.MEDIA_ROOT / name / filename
    if not image_path.is_file():
        logger.warning("Gallery image does not exist: %s", image_path)
        return None

    supported_languages = {code for code, _label in settings.LANGUAGES}
    for code in alts:
        if code not in supported_languages:
            logger.warning("Unsupported gallery language code %r for %s", code, image_path)

    stem = Path(filename).stem
    return GalleryItem(
        id=f"{name}-{stem}".replace("_", "-"),
        url=f"{settings.MEDIA_URL}{name}/{filename}",
        alts={code: alt.strip() for code, alt in alts.items()},
    )
