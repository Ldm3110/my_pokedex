from rest_framework import serializers

from .models import Pokemon
from .models import FavObject
from authentication.serializers import UserSerializer
from pokedex.serializers import PokedexCreatureDetailSerializer


class PokemonSerializer(serializers.ModelSerializer):
    """Serializer of Pokemon object"""

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "pokedex_creature",
            "trainer",
            "nickname",
            "level",
            "experience",
            "favorite_object"
        )
        read_only_fields = ("id", "level", "favorite_object")

    def validate(self, attrs):
        """Add pokemon nickname if no nickname is given and random favorite object"""
        nickname = attrs.get("nickname")
        pokedex_creature = attrs.get("pokedex_creature")
        if not nickname:
            attrs["nickname"] = pokedex_creature.name
        return super().validate(attrs)


class FavoriteObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavObject
        fields = '__all__'


class PokemonDetailsSerializer(serializers.ModelSerializer):
    pokedex_creature = PokedexCreatureDetailSerializer()
    trainer = UserSerializer()
    favorite_object = FavoriteObjectSerializer()

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "nickname",
            "level",
            "experience",
            "pokedex_creature",
            "trainer",
            "favorite_object"
        )


class PokemonGiveXPSerializer(serializers.Serializer):
    """Serializer of give-xp endpoint"""

    amount = serializers.IntegerField(min_value=0)
