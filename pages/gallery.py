from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import imagesize
import nestedtext
from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GalleryItem:
    id: str
    url: str
    alts: dict[str, str]
    width: int
    height: int


@cache
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


def parse_gallery_item(name: str, filename: str, alts: dict[str, str] | str) -> GalleryItem | None:
    image_path = settings.MEDIA_ROOT / name / filename
    if not image_path.is_file():
        logger.warning("Gallery image does not exist: %s", image_path)
        return None

    if alts == "":
        alts = {}

    supported_languages = {code for code, _label in settings.LANGUAGES}
    for code in alts:
        if code not in supported_languages:
            logger.warning("Unsupported gallery language code %r for %s", code, image_path)

    stem = Path(filename).stem
    item_id = f"{name}-{stem}".replace("/", "-").replace("_", "-")
    width, height = image_size(image_path)
    return GalleryItem(
        id=item_id,
        url=f"{settings.MEDIA_URL}{name}/{filename}",
        alts={code: alt.strip() for code, alt in alts.items()},
        width=width,
        height=height,
    )


def image_size(path: Path) -> tuple[int, int]:
    width, height = imagesize.get(path)
    if width < 0 or height < 0:
        logger.warning("Could not read image dimensions: %s", path)
        return 0, 0
    return width, height
