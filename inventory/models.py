from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Person(models.Model):
    """A real-world person known to the inventory system."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="person",
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    """A catalogue entry for a thing GEST can own, lend, or generally track."""

    class Type(models.TextChoices):
        BOARD_GAME = "board_game", "Board game"
        TTRPG = "ttrpg", "TTRPG asset"
        TCG = "tcg", "TCG"
        OFFICE = "office", "Office"
        OTHER = "other", "Other"

    type = models.CharField(max_length=32, choices=Type, db_index=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image_ref = models.CharField(max_length=500, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ItemCopy(models.Model):
    """A stored holding of an item, possibly representing more than one unit."""

    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="copies")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    owner = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="owned_copies")
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "item copy"
        verbose_name_plural = "item copies"

    def __str__(self) -> str:
        return f"{self.quantity} x {self.item}"


class BoardGame(Item):
    """An item subtype for board games and board-game expansions."""

    bgg_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    min_players = models.PositiveSmallIntegerField(null=True, blank=True)
    max_players = models.PositiveSmallIntegerField(null=True, blank=True)
    min_playtime_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    max_playtime_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    parent_game = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expansions",
    )

    class Meta:
        verbose_name = "board game"
        verbose_name_plural = "board games"


class TtrpgAsset(Item):
    """An item subtype for tabletop RPG books, figures, and other assets."""

    class System(models.TextChoices):
        DND = "dnd", "Dungeons & Dragons"
        PATHFINDER = "pathfinder", "Pathfinder"
        LOTR = "lotr", "The Lord of the Rings"
        OTHER = "other", "Other"

    system = models.CharField(max_length=32, choices=System)
    year = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "TTRPG asset"
        verbose_name_plural = "TTRPG assets"


class Lease(models.Model):
    """A checkout record for an item copy borrowed by a person."""

    copy = models.ForeignKey(ItemCopy, on_delete=models.PROTECT, related_name="leases")
    lessee = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="leases")
    checkout_time = models.DateTimeField(default=timezone.now)
    return_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-checkout_time"]

    def __str__(self) -> str:
        return f"{self.copy} leased to {self.lessee}"


class GameNightRequest(models.Model):
    """An aggregate request for an item on a game-night date."""

    date = models.DateField()
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="gamenight_requests")
    times = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["date", "item"], name="unique_gamenight_request")
        ]
        ordering = ["-date", "item__name"]

    def __str__(self) -> str:
        return f"{self.item} requested {self.times} times for {self.date}"


class GameNightGame(models.Model):
    """A record of an item copy taken to a game night."""

    date = models.DateField()
    copy = models.ForeignKey(ItemCopy, on_delete=models.PROTECT, related_name="gamenight_games")

    class Meta:
        ordering = ["-date", "copy__item__name"]

    def __str__(self) -> str:
        return f"{self.copy} taken on {self.date}"
