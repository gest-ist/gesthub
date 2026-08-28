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
    help = "Import tags, people or items from a CSV."

    @staticmethod
    def val(row, field):
        return row.get(field, "").strip()

    @classmethod
    def to_int(cls, row, field):
        value = cls.val(row, field)
        return int(value) if value else None

    @classmethod
    def to_decimal(cls, row, field):
        value = cls.val(row, field)
        return Decimal(value) if value else None

    @classmethod
    def to_bool(cls, row, field, default=False):
        value = cls.val(row, field).lower()

        if not value:
            return default

        return value in {"1", "true", "yes", "y"}

    def add_arguments(self, parser):
        parser.add_argument("--items")
        parser.add_argument("--tags")
        parser.add_argument("--people")

        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete imported data before importing.",
        )

    def read_csv(self, csv_file):
        with open(csv_file, newline="", encoding="utf-8-sig") as f:
            yield from csv.DictReader(f)

    @transaction.atomic
    def handle(self, *args, **options):

        if options["clear"]:
            self.clear_database(options)

        if options["tags"]:
            self.import_tags(options["tags"])

        if options["people"]:
            self.import_people(options["people"])

        if options["items"]:
            self.import_items(options["items"])

    def clear_database(self, options):
        if Lease.objects.exists():
            raise CommandError(
                "Cannot --clear while leases exist."
            )

        if options["items"]:
            ItemCopy.objects.all().delete()
            BoardGame.objects.all().delete()
            TtrpgAsset.objects.all().delete()
            Item.objects.all().delete()

        if options["tags"]:
            Tag.objects.all().delete()

        if options["people"]:
            Person.objects.exclude(pk=Person.GEST_ID).delete()

    def import_tags(self, csv_file):
        self.stdout.write(f"Importing tags from {csv_file}...")

        tags_created = 0

        for row in self.read_csv(csv_file):

            slug = self.val(row, "slug")

            if not slug:
                continue

            tag, created = Tag.objects.update_or_create(
                slug=slug,
                defaults={
                    "name_pt": self.val(row, "name_pt"),
                    "name_en": self.val(row, "name_en"),
                    "name_es": self.val(row, "name_es"),
                },
            )

            if created:
                tags_created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Tags imported: {tags_created}")
        )

    def import_people(self, csv_file):
        self.stdout.write(f"Importing people from {csv_file}...")

        people_created = 0

        for row in self.read_csv(csv_file):

            name = self.val(row, "name")

            if not name:
                continue

            person, created = Person.objects.update_or_create(
                name=name,
                defaults={
                    "email": self.val(row, "email"),
                    "notes": self.val(row, "notes"),
                },
            )

            if created:
                people_created += 1

        self.stdout.write(
            self.style.SUCCESS(f"People imported: {people_created}")
        )

    def import_items(self, csv_file):
        gest = Person.objects.get(pk=Person.GEST_ID)

        boardgame_lookup = {}
        pending_parents = []

        items_created = 0
        copies_created = 0
        tags_created = 0

        for row in self.read_csv(csv_file):

            #
            # Find existing Item
            #

            item = None

            if self.val(row,"type") == Item.Type.BOARD_GAME and self.to_int(row, "bgg_id"):

                try:
                    bg = BoardGame.objects.get(bgg_id=self.to_int(row, "bgg_id"))
                    item = Item.objects.get(pk=bg.pk)

                except BoardGame.DoesNotExist:
                    pass

            if item is None:
                item = Item.objects.filter(
                    type=self.val(row, "type"),
                    name=self.val(row, "name"),
                ).first()

            #
            # Create Item if necessary
            #

            if item is None:

                bgg_id = self.to_int(row, "bgg_id")

                thumbnail_ref = self.val(row, "thumbnail_ref")
                image_ref = self.val(row, "image_ref")

                if bgg_id:
                    thumbnail_ref = f"bgimg/thmb/{bgg_id}.avif"
                    image_ref = f"bgimg/img/{bgg_id}.avif"

                item = Item.objects.create(
                    type=self.val(row, "type"),
                    name=self.val(row, "name"),
                    price=self.to_decimal(row, "price"),
                    thumbnail_ref=thumbnail_ref,
                    image_ref=image_ref,
                    notes=self.val(row, "notes"),
                )

                items_created += 1

                #
                # Tags
                #

                tags = [
                    t.strip()
                    for t in self.val(row, "tags").split(";")
                    if t.strip()
                ]

                for slug in tags:

                    tag, created = Tag.objects.get_or_create(
                        slug=slug,
                        defaults={
                            "name_pt": slug.replace("-", " ").title(),
                            "name_en": slug.replace("-", " ").title(),
                            "name_es": slug.replace("-", " ").title(),
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
                        bgg_id=self.to_int(row, "bgg_id"),
                        year=self.to_int(row, "year"),
                        weight=self.to_decimal(row, "weight"),
                        min_players=self.to_int(row, "min_players"),
                        max_players=self.to_int(row, "max_players"),
                        opt_players=self.to_int(row, "opt_players"),
                        min_playtime_minutes=self.to_int(row, "min_playtime_minutes"),
                        max_playtime_minutes=self.to_int(row, "max_playtime_minutes"),
                        rating=self.to_decimal(row, "rating"),
                    )

                    bg.save_base(raw=True)

                    boardgame_lookup[item.name.strip().casefold()] = bg

                    if self.val(row, "parent_game"):
                        pending_parents.append(
                            (bg, self.val(row, "parent_game").strip().casefold())
                        )

                #
                # TTRPG subtype
                #

                elif item.type == Item.Type.TTRPG:

                    asset = TtrpgAsset(
                        item_ptr=item,
                        system=self.val(row, "system") or TtrpgAsset.System.OTHER,
                        year=self.to_int(row, "year"),
                    )
                    asset.save_base(raw=True)

            elif item.type == Item.Type.BOARD_GAME:
                bg = BoardGame.objects.get(pk=item.pk)

                boardgame_lookup[item.name.strip().casefold()] = bg

                if self.val(row, "parent_game"):
                    pending_parents.append(
                        (bg, self.val(row, "parent_game").strip().casefold())
                    )

            #
            # Owner
            #

            owner_name = self.val(row, "owner")

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
                quantity=self.to_int(row, "quantity") or 1,
                owner=owner,
                location=self.val(row, "location"),
                hidden=self.to_bool(row, "hidden", default=False),
                notes=self.val(row, "notes"),
            )

            copies_created += 1

        #
        # Resolve expansions
        #

        for bg, parent_name in pending_parents:

            parent = boardgame_lookup.get(parent_name)

            if parent:
                bg.parent_game = parent
                bg.save(update_fields=["parent_game"])
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
