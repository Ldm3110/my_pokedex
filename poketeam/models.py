from django.db import models
from django.conf import settings

# Create your models here.


class Poketeam(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = "Poketeam"
        verbose_name_plural = "Poketeams"

    def __str__(self) -> str:
        return f"{self.name} trained by {self.trainer}"
