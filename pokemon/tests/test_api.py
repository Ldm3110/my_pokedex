import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Pokemon
from ..serializers import PokemonSerializer, PokemonDetailsSerializer

pytestmark = pytest.mark.django_db


class TestPokemonActions:

    def test_listing_pokemons(self, user_log, client_log, pokemon_factory):
        """Test listing Pokedex creatures."""

        # Create 3 pokemons
        pokemon_factory()
        pokemon_factory(trainer=user_log)
        pokemon_factory()

        # Unauthenticated user should be denied access
        res = APIClient().get(reverse("pokemon:pokemon-list"))
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        # Authenticated user should be given access
        res = client_log.get(reverse("pokemon:pokemon-list"))
        assert res.status_code == status.HTTP_200_OK

        pokemons = Pokemon.objects.filter(trainer=user_log.id)
        serializer = PokemonSerializer(pokemons, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert len(serializer.data) == 1
        assert serializer.data == res.data.get('results')

    def test_view_pokemon_detail(self, user_log, client_log, pokemon_factory):
        """Test retrieving a Pokemon creature"""

        # Create 2 pokemons
        pokemon_factory()
        pokemon = pokemon_factory(trainer=user_log)

        # Unauthenticated user should be denied access
        res = APIClient().get(
            reverse("pokemon:pokemon-detail", args=[pokemon.id]))
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        # Authenticated user should be given access
        res = client_log.get(
            reverse("pokemon:pokemon-detail", args=[pokemon.id]))
        assert res.status_code == status.HTTP_200_OK

        serializer = PokemonDetailsSerializer(pokemon)

        assert res.status_code == status.HTTP_200_OK
        assert serializer.data == res.data

    def test_create_pokemon(
        self,
        user_log,
        client_log,
        pokedex_creature_factory,
        pokemon_factory,
    ):
        """Authenticated user can create a pokermon"""
        creature = pokedex_creature_factory(name="Brown Bear")
        pokemon_factory()
        pokemon_factory()

        # Create a trained pokemon
        payload = {
            "pokedex_creature": creature.id,
            "trainer": user_log.id,
            "nickname": "Gozilla",
        }
        res = client_log.post(
            reverse("pokemon:pokemon-list"),
            payload,
        )
        assert res.status_code == status.HTTP_201_CREATED

        pokemon = Pokemon.objects.get(id=res.data["id"])
        assert str(pokemon) == "Gozilla (tai)"
        assert pokemon.pokedex_creature.name == "Brown Bear"

        # Create a wild pokemon
        payload = {
            "pokedex_creature": creature.id,
        }
        res = client_log.post(
            reverse("pokemon:pokemon-list"),
            payload,
        )
        assert res.status_code == status.HTTP_201_CREATED

        pokemon = Pokemon.objects.get(id=res.data["id"])
        assert str(pokemon) == "Brown Bear (wild)"

    def test_partial_update_pokemon(self, client_log, pokemon_factory):
        """Authenticated user can update an existing pokemon with patch"""
        pokemon = pokemon_factory(nickname="Lion")
        payload = {"nickname": "Monster king"}
        res = client_log.patch(
            reverse("pokemon:pokemon-detail", args=[pokemon.id]),
            payload,
        )
        assert res.status_code == status.HTTP_200_OK
        pokemon.refresh_from_db()
        assert pokemon.nickname == payload["nickname"]

    def test_full_update_pokemon(
        self, client_log, user_log, pokedex_creature_factory, pokemon_factory
    ):
        """Authenticated user can update an existing pokemon with put"""
        pokemon = pokemon_factory()
        creature = pokedex_creature_factory()
        payload = {
            "nickname": "Monster king",
            "trainer": user_log.id,
            "pokedex_creature": creature.id,
        }
        res = client_log.put(
            reverse("pokemon:pokemon-detail", args=[pokemon.id]),
            payload,
        )
        assert res.status_code == status.HTTP_200_OK
        pokemon.refresh_from_db()
        assert pokemon.nickname == payload["nickname"]
        assert pokemon.trainer == user_log
        assert pokemon.pokedex_creature == creature

    def test_delete_pokemon(self, client_log, pokemon_factory):
        """Authenticated user can delete an existing pokermon"""
        pokemon = pokemon_factory()

        res = client_log.delete(
            reverse("pokemon:pokemon-detail", args=[pokemon.id]))
        assert res.status_code == status.HTTP_204_NO_CONTENT

        assert not Pokemon.objects.filter(id=pokemon.id).exists()

    def test_give_xp_to_pokemon(self, client_log, pokemon_factory):
        """Authenticated user can give XP to an existing pokermon"""
        pokemon = pokemon_factory(level=1, experience=40)

        payload = {
            "amount": 150,
        }
        res = client_log.post(
            reverse("pokemon:pokemon-give-xp", args=[pokemon.id]),
            payload,
        )
        assert res.status_code == status.HTTP_200_OK

        pokemon = Pokemon.objects.get(id=pokemon.id)
        pokemon.refresh_from_db()

        assert pokemon.level == 2
        assert pokemon.experience == 190

    def test_give_xp_to_pokemon_invalid_request(self, client_log, pokemon_factory):
        """Authenticated user can give XP to an existing pokermon"""
        pokemon = pokemon_factory(level=1, experience=40)

        payload = {
            "amount": "Hello",
        }
        res = client_log.post(
            reverse("pokemon:pokemon-give-xp", args=[pokemon.id]),
            payload,
        )
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.data == {
            'amount': [
                'A valid integer is required.'
            ]
        }

        payload = {
            "attack": 100,
        }
        res = client_log.post(
            reverse("pokemon:pokemon-give-xp", args=[pokemon.id]),
            payload,
        )
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.data == {
            "amount": [
                "This field is required."
            ]
        }


class TestFavoriteObjectActions:
    def test_listing_favorite_object(self, user_log, client_log):
        # Unauthenticated user should be denied access
        res = APIClient().get(reverse("favobject-list"))
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        # Authenticated user should be given access
        res = client_log.get(reverse("favobject-list"))
        assert res.status_code == status.HTTP_200_OK

    def test_listing_detail_favorite_object_with_id(
            self,
            user_log,
            client_log,
            fav_object_factory):

        # Create 2 favorite object
        object_1 = fav_object_factory()
        fav_object_factory()

        # Unauthenticated user should be denied access
        res = APIClient().get(
            reverse("pokemon:favobject-id", args=[object_1.id]))
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        # Authenticated user should be given access
        res = client_log.get(
            reverse("pokemon:favobject-id", args=[object_1.id]))
        assert res.status_code == status.HTTP_200_OK

    """ Doesn´t work actually ...
    def test_listing_detail_favorite_object_with_search_field(
        self,
        client_log,
        user_log,
        fav_object_factory
    ):
        # create an object
        obj = fav_object_factory()
        print(obj)
        karg = {"search": obj.name}
        
        # Unauthenticated user should be denied access
        res = APIClient().get(
            reverse("favobject-list", kwargs=karg))
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Authenticated user should be given access
        res = client_log.get(
            reverse("favobject-list", kwargs=karg))
        assert res.status_code == status.HTTP_200_OK """
