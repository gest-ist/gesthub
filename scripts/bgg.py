# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "bgg-api>=1.1.18,<2",
#   "wand>=0.7.2",
#   "python-dotenv>=1.2.2",
# ]
# ///

"""Fetch BoardGameGeek metadata, download box images, and optimize them.

...
"""

from __future__ import annotations
from boardgamegeek import BGGClient
import dotenv

import argparse
import itertools
import json
import os
import re
import sys
from concurrent.futures import Executor, ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from typing import Callable

import boardgamegeek
import requests
from boardgamegeek.objects import BoardGame
from wand.image import Image

ID_RE = re.compile(r"[0-9]+")
EXTENSIONS = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
RESIZE_AREA = 1000**2
FINAL_FORMAT = "avif"
QUALITY = 40  # 40% ?


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
    parser = argparse.ArgumentParser(description=__doc__)

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
        print(f"\tFetching box image for game \"{game.name}\" ({game.id})")
        with requests.get(game.image, stream=True) as resp:
            resp.raise_for_status()
            with (raw_images_path / str(game.id)).with_suffix(".jpg").open("wb") as fp:
                for chunk in resp.iter_content(2**13):
                    fp.write(chunk)

    print("Fetching images")
    for game in games:
        if game.image:
            pe.submit(fetch, game)


def process_image(raw_path: Path, final_path: Path):
    print(f"\tProcessing image {raw_path.stem}")
    with Image(filename=raw_path) as img:
        img: Image = img
        img.format = FINAL_FORMAT
        img.transform(resize=f"{RESIZE_AREA}@")
        img.compression_quality = QUALITY
        img.save(filename=final_path)


def process_images(raw_images_path: Path, final_images_path: Path, *, pe: Executor):
    raw_images_path.mkdir(parents=True, exist_ok=True)
    final_images_path.mkdir(parents=True, exist_ok=True)

    print("Processing images")
    for file in raw_images_path.iterdir():
        if file.is_file():
            final_path = (final_images_path / file.stem).with_suffix(f".{FINAL_FORMAT}")
            pe.submit(process_image, file, final_path)


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
        process_images(args.raw_images, args.final_images, pe=ppe)
        ppe.shutdown()

    print("Done")


if __name__ == "__main__":
    try:
        dotenv.load_dotenv()
        main(parse_args())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        exit(1)
