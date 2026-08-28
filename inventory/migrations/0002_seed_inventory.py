from __future__ import annotations

from django.db import migrations



def seed_inventory(apps, schema_editor):
    Person = apps.get_model("inventory", "Person")

    gest = Person.objects.update_or_create(
        id=0,
        defaults={
            "name": "GEST",
            "email": "gest.sa@aeist.pt",
            "notes": "Inventário pertencente ao grupo.",
        },
    )[0]

def unseed_inventory(apps, schema_editor):
    Person = apps.get_model("inventory", "Person")
    Person.objects.filter(name__in=["GEST"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_inventory, unseed_inventory),
    ]
