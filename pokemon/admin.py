from django.contrib import admin

from pokemon.models import Pokemon, FavObject


class PokemonAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Pokemon._meta.fields if field.name != "id"]
    ordering = ("pokedex_creature__ref_number",)
    search_fields = ("nickname", "trainer__username")
    list_per_page = 50

    autocomplete_fields = ("pokedex_creature", "trainer")


class FavObjectAdmin(admin.ModelAdmin):
    model = FavObject
    ordering = ("id", )
    list_per_page = 50
    search_fields = ("name", )
    list_display = ("id", "name", "img_uri")


admin.site.register(FavObject, FavObjectAdmin)
admin.site.register(Pokemon, PokemonAdmin)
