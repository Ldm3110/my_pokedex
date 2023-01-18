from django.contrib import admin

from .models import Poketeam


class PoketeamAdmin(admin.ModelAdmin):
    model = Poketeam


admin.register(PoketeamAdmin, Poketeam)
