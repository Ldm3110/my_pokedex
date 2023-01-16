from rest_framework.serializers import ModelSerializer, RelatedField

from .models import Poketeam
from pokemon.serializers import PokemonSerializer


class PoketeamSerializer(ModelSerializer):

    class Meta:
        model = Poketeam
        fields = "__all__"
        read_only_fields = ('id', 'trainer', )


class PoketeamListSerializer(ModelSerializer):

    class Meta:
        model = Poketeam
        fields = ['id', ]
        

class PokemonListingField(RelatedField):
    def to_representation(self, value):
        serialized_data = PokemonSerializer(value)
        return serialized_data.data
        

class PoketeamDetailSerializer(ModelSerializer):
    pokemon = PokemonListingField(many=True, read_only=True)

    class Meta:
        model = Poketeam
        fields = [
            'id',
            'name',
            'pokemon'
        ]
