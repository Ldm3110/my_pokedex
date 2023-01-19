from django.conf import settings
from django.db import models

from pokedex.models import PokedexCreature
from poketeam.models import Poketeam


class FavObject(models.Model):
    name = models.CharField(max_length=50)
    img_uri = models.URLField()
    description = models.TextField(max_length=250)

    class Meta:
        verbose_name = "Favorite Object"
        verbose_name_plural = "Favorite Objects"

    def __str__(self) -> str:
        return f"{self.name}"


class Pokemon(models.Model):
    """Pokemon object"""

    pokedex_creature = models.ForeignKey(
        PokedexCreature,
        on_delete=models.CASCADE,
    )

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    nickname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    level = models.PositiveSmallIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)
    favorite_object = models.ForeignKey(
        FavObject,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    team = models.ForeignKey(
        Poketeam,
        related_name="pokemon",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def clean(self):
        """
        Set default nickname to related pokedex creature name
        if no nickname is given
        """

        if not self.nickname:
            self.nickname = self.pokedex_creature.name
        return super().clean()

    def __str__(self):
        """
        Return Pokermon name with the trainer username if it has one

        Return Pokermon name (wild) if not
        """

        return "{} ({})".format(
            self.nickname, self.trainer.username if self.trainer else "wild"
        )

    def receive_xp(self, amount: int) -> None:
        """
        Update pokemon level based on the XP is received
        """
        self.experience += amount
        self.level = 1 + self.experience // 100
        self.save()

    def add_in_team(self, team: Poketeam):
        self.team = team
        self.save()

    def remove_from_team(self, team: Poketeam):
        self.team = None
        self.save()
