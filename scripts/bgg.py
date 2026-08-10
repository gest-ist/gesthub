#!/usr/bin/env -S uv run -s
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "bgg-api>=1.1.18,<2",
#   "wand>=0.7.2",
#   "python-dotenv>=1.2.2",
# ]
# ///

"""Fetch game data from BoardGameGeek, download box images, and optimize them.

It requires an env-var called BGG_TOKEN, with your BGG API token (should be an hexadecimal UUID string).
The script automatically loads an .env file if it exists.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
from concurrent.futures import Executor, ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from typing import Callable

import dotenv
import requests
from boardgamegeek import BGGClient
from boardgamegeek.objects import BoardGame
from wand.image import Image

RESIZE_AREA = 1000**2
FINAL_FORMAT = "avif"
QUALITY = 40  # 40% ?

EXAMPLES = """
Examples:
(recommended you run with: uv run scripts/bgg.py ...)

  Read game IDs from stdin, fetch data and write to var/games.jsonl:
  $ bgg.py --data var/games.jsonl --fetch-data

  Read game data from var/game.jsonl, fetch box images and write them to var/boxes/raw, one file per game:
  $ bgg.py --data var/games.jsonl --raw-images var/boxes/raw --fetch-images

  Transform all raw images from var/boxes/raw and write them to var/boxes/final, with default parameters:
  $ bgg.py --raw-images var/boxes/raw --final-images var/boxes/final

  Transform raw images into AVIF with resizing area of 500000 and 20% quality:
  $ bgg.py --raw-images var/boxes/raw --final-images var/boxes/final --final-area 500000 --final-quality 20

  Do all the pipeline stages:
  $ bgg.py --data var/games.jsonl --fetch-data --raw-images var/boxes/raw --fetch-images --final-images var/boxes/final
"""


def number[T: int | float = int](
    parse: Callable[[str], T] = int,  # ty:ignore[invalid-parameter-default]
    range: tuple[int | None, int | None] = (1, None),
) -> Callable[[str], T]:
    def inner(arg: str) -> T:
        n = parse(arg)
        match range:
            case (int(a), int(b)) if not a <= n <= b:
                raise argparse.ArgumentTypeError(f"must be between {a} and {b}")
            case (None, int(b)) if n > b:
                raise argparse.ArgumentTypeError(f"must be at most {b}")
            case (int(a), None) if n < a:
                raise argparse.ArgumentTypeError(f"must be at least {a}")
        return n

    return inner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, epilog=EXAMPLES
    )

    parser.add_argument("--data", type=Path, help="Path to JSONL containing game data")
    parser.add_argument(
        "--fetch-data",
        action="store_true",
        help="Fetch game data for the BGG IDs passed through stdin, and write to --data path",
    )

    parser.add_argument("--raw-images", type=Path, help="Path to directory containing raw images")
    parser.add_argument(
        "--fetch-images",
        action="store_true",
        help="Fetch raw images from the BGG ID for the games stored in --data, and write them to --raw-images",
    )

    parser.add_argument(
        "--final-images", type=Path, help="Path to directory containing the optimized images"
    )
    parser.add_argument("--final-format", default=FINAL_FORMAT, help="The final image format")
    parser.add_argument(
        "--final-quality",
        type=number(int, (0, 100)),
        default=QUALITY,
        help="The final image quality (percent)",
    )
    parser.add_argument(
        "--final-area",
        type=number(int),
        default=RESIZE_AREA,
        help="The final image area (height×width)",
    )

    parser.add_argument(
        "--jobs",
        "-j",
        type=number(int),
        help="The number of jobs/workers to use to fetch and process data",
    )

    return parser.parse_args()


def fetch_data(token: str, data_path: Path, ids: list[int], *, pe: Executor) -> list[BoardGame]:
    client = BGGClient(token)  # TODO: add timeout/retries/rpm

    def fetch(ids: tuple[int,]) -> list[BoardGame]:
        ids: list[int] = list(ids)
        print(f"\tFetching data for {ids}")
        return client.game_list(ids)

    print("Fetching game data")
    map = pe.map(fetch, itertools.batched(ids, 20))
    games = list(itertools.chain.from_iterable(map))

    # write JSONL
    print("All game data fetched, writing data JSONL")
    with data_path.open("w") as fp:
        fp.writelines(f"{json.dumps(game.data())}\n" for game in games)

    return games


def read_data(data_path: Path) -> list[BoardGame]:
    print("Reading game data from JSONL")
    with data_path.open() as fp:
        return [BoardGame(json.loads(line)) for line in fp]


def fetch_images(games: list[BoardGame], raw_images_path: Path, *, pe: Executor):
    raw_images_path.mkdir(parents=True, exist_ok=True)

    def fetch(game: BoardGame):
        url = game.image
        if url is None:
            print(f'\t! "{game.name}" ({game.id}) does not have an image URL')
            return

        print(f'\tFetching box image for game "{game.name}" ({game.id})')
        suffix_idx = url.rfind(".")
        suffix = url[suffix_idx:].lower() if suffix_idx != -1 else ".jpg"
        with requests.get(url, stream=True) as resp:
            resp.raise_for_status()
            with (raw_images_path / str(game.id)).with_suffix(suffix).open("wb") as fp:
                for chunk in resp.iter_content(2**13):
                    fp.write(chunk)

    print("Fetching images")
    for game in games:
        if game.image:
            pe.submit(fetch, game)


def process_image(
    raw_path: Path,
    final_path: Path,
    *,
    format: str = FINAL_FORMAT,
    quality: int = QUALITY,
    area: int = RESIZE_AREA,
):
    print(f"\tProcessing image {raw_path.stem}")
    with Image(filename=raw_path) as img:
        img: Image = img
        img.format = format
        img.transform(resize=f"{area}@")
        img.compression_quality = quality
        img.save(filename=final_path)


def process_images(
    raw_images_path: Path,
    final_images_path: Path,
    *,
    format: str = FINAL_FORMAT,
    quality: int = QUALITY,
    area: int = RESIZE_AREA,
    pe: Executor,
):
    raw_images_path.mkdir(parents=True, exist_ok=True)
    final_images_path.mkdir(parents=True, exist_ok=True)

    print("Processing images")
    for file in raw_images_path.iterdir():
        if file.is_file():
            final_path = (final_images_path / file.stem).with_suffix(f".{format}")
            pe.submit(process_image, file, final_path, format=format, quality=quality, area=area)


def main(args: argparse.Namespace):
    tpe = ThreadPoolExecutor(max_workers=args.jobs)

    data: list[BoardGame] = []
    if args.fetch_data:
        assert args.data, "Must provide data path"
        data = fetch_data(os.environ["BGG_TOKEN"], args.data, [int(n) for n in sys.stdin], pe=tpe)
    elif args.data:
        data = read_data(args.data)

    if args.fetch_images:
        assert args.raw_images, "Must profile raw image dir"
        assert args.data, "Must provide data path"
        fetch_images(data, args.raw_images, pe=tpe)

    tpe.shutdown()

    if args.final_images:
        assert args.raw_images, "Must provide raw images dir"
        ppe = ProcessPoolExecutor(max_workers=args.jobs)
        process_images(
            args.raw_images,
            args.final_images,
            format=args.final_format,
            quality=args.final_quality,
            area=args.final_area,
            pe=ppe,
        )
        ppe.shutdown()

    print("Done")


if __name__ == "__main__":
    try:
        dotenv.load_dotenv()
        main(parse_args())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        exit(1)
