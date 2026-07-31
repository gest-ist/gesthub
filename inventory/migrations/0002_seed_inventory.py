from __future__ import annotations

from decimal import Decimal

from django.db import migrations
from django.utils import timezone


TAGS = {
    "familiar": ("Familiar", "Family"),
    "estrategia": ("Estratégia", "Strategy"),
    "party": ("Party", "Party"),
    "iniciacao": ("Iniciação", "Gateway"),
    "rpg": ("RPG", "RPG"),
}

BOARDGAMES = [
    {
        "name": "Catan",
        "bgg_id": 13,
        "year": 1995,
        "weight": Decimal("2.30"),
        "min_players": 3,
        "max_players": 4,
        "opt_players": 4,
        "min_playtime_minutes": 60,
        "max_playtime_minutes": 120,
        "rating": Decimal("7.1"),
        "tags": ["familiar", "estrategia", "iniciacao"],
    },
    {
        "name": "Wavelength",
        "bgg_id": 262543,
        "year": 2019,
        "weight": Decimal("1.12"),
        "min_players": 2,
        "max_players": 12,
        "min_playtime_minutes": 30,
        "max_playtime_minutes": 45,
        "rating": Decimal("7.4"),
        "tags": ["party", "iniciacao"],
        "third_party_owner": True,
    },
    {
        "name": "HEAT: Pedal to the Metal",
        "bgg_id": 366013,
        "year": 2022,
        "weight": Decimal("2.19"),
        "min_players": 1,
        "max_players": 6,
        "min_playtime_minutes": 30,
        "max_playtime_minutes": 60,
        "rating": Decimal("8.1"),
        "tags": ["familiar", "estrategia"],
        "leased": True,
    },
    {
        "name": "Brass",
        "bgg_id": 28720,
        "year": 2007,
        "weight": Decimal("3.86"),
        "min_players": 3,
        "max_players": 4,
        "min_playtime_minutes": 120,
        "max_playtime_minutes": 180,
        "rating": Decimal("7.9"),
        "tags": ["estrategia"],
    },
]

TTRPG_ASSETS = [
    {
        "name": "D&D Player's Handbook",
        "system": "dnd",
        "year": 2014,
        "tags": ["rpg"],
    },
    {
        "name": "The One Ring Core Rules",
        "system": "lotr",
        "year": 2022,
        "tags": ["rpg"],
    },
]


def seed_inventory(apps, schema_editor):
    Person = apps.get_model("inventory", "Person")
    Tag = apps.get_model("inventory", "Tag")
    BoardGame = apps.get_model("inventory", "BoardGame")
    TtrpgAsset = apps.get_model("inventory", "TtrpgAsset")
    ItemCopy = apps.get_model("inventory", "ItemCopy")
    Lease = apps.get_model("inventory", "Lease")

    tags = {
        slug: Tag.objects.update_or_create(
            slug=slug,
            defaults={"name_pt": name_pt, "name_en": name_en},
        )[0]
        for slug, (name_pt, name_en) in TAGS.items()
    }

    gest = Person.objects.update_or_create(
        id=0,
        defaults={
            "name": "GEST",
            "email": "gest.sa@aeist.pt",
            "notes": "Inventário pertencente ao grupo.",
        },
    )[0]
    third_party = Person.objects.update_or_create(
        name="Sara Um",
        defaults={
            "email": "sara1@example.test",
            "notes": "Pessoa fictícia que cedeu jogos ao GEST.",
        },
    )[0]
    lessee = Person.objects.update_or_create(
        name="Sara dois",
        defaults={
            "email": "sara2@example.test",
            "notes": "Pessoa fictícia para dados de exemplo.",
        },
    )[0]

    for data in BOARDGAMES:
        fields = data.copy()
        tag_slugs = fields.pop("tags")
        leased = fields.pop("leased", False)
        third_party_owner = fields.pop("third_party_owner", False)
        fields["image_ref"] = f"bgimg/img/{fields['bgg_id']}.avif"
        fields["thumbnail_ref"] = f"bgimg/thmb/{fields['bgg_id']}.avif"
        item = BoardGame.objects.update_or_create(
            name=fields["name"],
            defaults={"type": "board_game", **fields},
        )[0]
        item.tags.set([tags[slug] for slug in tag_slugs])
        copy = ItemCopy.objects.update_or_create(
            item=item,
            owner=third_party if third_party_owner else gest,
            location="Sala GEST",
            defaults={"quantity": 1, "hidden": False},
        )[0]
        if leased:
            Lease.objects.update_or_create(
                copy=copy,
                lessee=lessee,
                return_time=None,
                defaults={
                    "checkout_time": timezone.now(),
                    "notes": "Empréstimo fictício para testar estado indisponível.",
                },
            )

    for data in TTRPG_ASSETS:
        fields = data.copy()
        tag_slugs = fields.pop("tags")
        item = TtrpgAsset.objects.update_or_create(
            name=fields["name"],
            defaults={"type": "ttrpg", **fields},
        )[0]
        item.tags.set([tags[slug] for slug in tag_slugs])
        ItemCopy.objects.update_or_create(
            item=item,
            owner=gest,
            location="Armário RPG",
            defaults={"quantity": 1, "hidden": False},
        )


def unseed_inventory(apps, schema_editor):
    Person = apps.get_model("inventory", "Person")
    Tag = apps.get_model("inventory", "Tag")
    Item = apps.get_model("inventory", "Item")
    ItemCopy = apps.get_model("inventory", "ItemCopy")
    Lease = apps.get_model("inventory", "Lease")

    items = Item.objects.filter(name__in=[item["name"] for item in [*BOARDGAMES, *TTRPG_ASSETS]])
    Lease.objects.filter(copy__item__in=items).delete()
    ItemCopy.objects.filter(item__in=items).delete()
    items.delete()
    Person.objects.filter(name__in=["GEST", "Alice Silva", "Carlos Pereira"]).delete()
    Tag.objects.filter(slug__in=TAGS).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_inventory, unseed_inventory),
    ]
