import csv
from decimal import Decimal

from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import transaction

from inventory.models import (
    BoardGame,
    Item,
    ItemCopy,
    Lease,
    Person,
    Tag,
    TtrpgAsset,
)


class Command(BaseCommand):
    help = "Import inventory from a master CSV."

    def add_arguments(self, parser):
        parser.add_argument("csv_file")
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all inventory before importing.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        if options["clear"]:
            self.stdout.write("Clearing existing inventory...")

            if Lease.objects.exists():
                raise CommandError(
                    "Cannot --clear while leases exist. Delete them manually if this is intentional."
                )

            ItemCopy.objects.all().delete()
            BoardGame.objects.all().delete()
            TtrpgAsset.objects.all().delete()
            Item.objects.all().delete()
            Tag.objects.all().delete()

        gest = Person.objects.get(pk=Person.GEST_ID)

        boardgame_lookup = {}
        pending_parents = []

        items_created = 0
        copies_created = 0
        tags_created = 0

        with open(csv_file, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:

                def val(name):
                    return row.get(name, "").strip()

                def to_int(name):
                    v = val(name)
                    return int(v) if v else None

                def to_decimal(name):
                    v = val(name)
                    return Decimal(v) if v else None

                def to_bool(name, default=False):
                    v = val(name).lower()

                    if not v:
                        return default

                    return v in ("1", "true", "yes", "y")

                #
                # Find existing Item
                #

                item = None

                if val("type") == Item.Type.BOARD_GAME and to_int("bgg_id"):

                    try:
                        bg = BoardGame.objects.get(bgg_id=to_int("bgg_id"))
                        item = Item.objects.get(pk=bg.pk)

                    except BoardGame.DoesNotExist:
                        pass

                if item is None:
                    item = Item.objects.filter(
                        type=val("type"),
                        name=val("name"),
                    ).first()

                #
                # Create Item if necessary
                #

                if item is None:

                    item = Item.objects.create(
                        type=val("type"),
                        name=val("name"),
                        price=to_decimal("price"),
                        thumbnail_ref=val("thumbnail_ref"),
                        image_ref=val("image_ref"),
                        notes=val("notes"),
                    )

                    items_created += 1

                    #
                    # Tags
                    #

                    tags = [
                        t.strip()
                        for t in val("tags").split(";")
                        if t.strip()
                    ]

                    for slug in tags:

                        tag, created = Tag.objects.get_or_create(
                            slug=slug,
                            defaults={
                                "name_pt": slug.replace("-", " ").title(),
                                "name_en": slug.replace("-", " ").title(),
                            },
                        )

                        if created:
                            tags_created += 1

                        item.tags.add(tag)

                    #
                    # Board game subtype
                    #

                    if item.type == Item.Type.BOARD_GAME:

                        bg = BoardGame(
                            item_ptr=item,
                            bgg_id=to_int("bgg_id"),
                            year=to_int("year"),
                            weight=to_decimal("weight"),
                            min_players=to_int("min_players"),
                            max_players=to_int("max_players"),
                            opt_players=to_int("opt_players"),
                            min_playtime_minutes=to_int("min_playtime_minutes"),
                            max_playtime_minutes=to_int("max_playtime_minutes"),
                            rating=to_decimal("rating"),
                        )

                        bg.save_base(raw=True)

                        boardgame_lookup[item.name.strip().casefold()] = bg

                        if val("parent_game"):
                            pending_parents.append(
                                (bg, val("parent_game").strip().casefold())
                            )

                    #
                    # TTRPG subtype
                    #

                    elif item.type == Item.Type.TTRPG:

                        asset = TtrpgAsset(
                            item_ptr=item,
                            system=val("system") or TtrpgAsset.System.OTHER,
                            year=to_int("year"),
                        )
                        asset.save_base(raw=True)

                elif item.type == Item.Type.BOARD_GAME:
                    bg = BoardGame.objects.get(pk=item.pk)

                    boardgame_lookup[item.name.strip().casefold()] = bg

                    if val("parent_game"):
                        pending_parents.append(
                            (bg, val("parent_game").strip().casefold())
                        )

                #
                # Owner
                #

                owner_name = val("owner")

                if owner_name:

                    owner, _ = Person.objects.get_or_create(
                        name=owner_name,
                    )

                else:
                    owner = gest

                #
                # Create copy
                #

                ItemCopy.objects.create(
                    item=item,
                    quantity=to_int("quantity") or 1,
                    owner=owner,
                    location=val("location"),
                    hidden=to_bool("hidden", default=False),
                    notes=val("notes"),
                )

                copies_created += 1

        #
        # Resolve expansions
        #

        for bg, parent_name in pending_parents:

            parent = boardgame_lookup.get(parent_name)

            if parent:
                bg.parent_game = parent
                bg.save()
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Parent game '{parent_name}' not found."
                    )
                )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Import complete."))
        self.stdout.write(f"Items created : {items_created}")
        self.stdout.write(f"Copies created: {copies_created}")
        self.stdout.write(f"Tags created  : {tags_created}")