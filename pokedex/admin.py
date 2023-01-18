from django.contrib import admin

from pokemon.models import PokedexCreature


class PokedexCreatureAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in PokedexCreature._meta.fields if field.name != "id"
    ]
    ordering = ("ref_number",)
    search_fields = ("name",)
    list_per_page = 50


admin.site.register(PokedexCreature, PokedexCreatureAdmin)
