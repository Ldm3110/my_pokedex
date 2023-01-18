import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestPoketeamActions:
    """
    Some tests for poketeam actions
    """
    poketeam_list = "poketeam-list"
    poketeam_detail = "poketeam-detail"
    pokemon_add = "poketeam-add-pokemon"
    pokemon_remove = "poketeam-remove-pokemon"

    def test_listing_my_teams(
        self,
        user_log,
        client_log,
        poketeam_factory
    ):
        # create a poketeam with user_log like trainer
        poketeam_factory(trainer=user_log)

        # access denied if user is not authenticated
        res = APIClient().get(reverse(self.poketeam_list))
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        # status 200 il user is authenticated
        res = client_log.get(
            reverse(
                self.poketeam_list
            )
        )
        expected_return = {
            "id": 1
        }

        assert res.status_code == status.HTTP_200_OK
        assert expected_return == res.data["results"][0]

    def test_listing_specific_team(
        self,
        user_log,
        client_log,
        poketeam_factory,
        pokemon_factory
    ):

        # create a poketeam with user_log like trainer
        poketeam = poketeam_factory(trainer=user_log)

        # create a pokemon trained by the user
        pokemon_factory(
            trainer=user_log,
            team=poketeam
        )

        # access denied if user is not authenticated
        res = APIClient().get(
            reverse(
                self.poketeam_detail,
                args=[poketeam.id]
            )
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        # status 200 il user is authenticated
        res = client_log.get(
            reverse(
                self.poketeam_detail,
                args=[poketeam.id]
            )
        )
        assert res.status_code == status.HTTP_200_OK

    def test_create_poketeam(
        self,
        user_log,
        client_log,
    ):
        """
        Create a new poketeam Confirm the team is attached to the client_log
        """

        payload = {
            "name": "NewPoketeam test"
        }

        expected_return = {
            "id": 3,
            "name": "NewPoketeam test",
            "trainer": user_log.id,
        }

        res = client_log.post(
            reverse(self.poketeam_list),
            payload
        )
        assert res.status_code == status.HTTP_201_CREATED
        assert res.data == expected_return

    def test_add_pokemon_on_a_team(
        self,
        client_log,
        user_log,
        poketeam_factory,
        pokemon_factory
    ):
        """
        Test the possibilities for the user to add a pokemon in his team
        """
        # create a pokemon and a team for the same trainer
        pokemon = pokemon_factory(
            trainer=user_log
        )
        poketeam = poketeam_factory(
            trainer=user_log
        )

        payload = {
            "pokemon": pokemon.id
        }

        res = client_log.patch(
            reverse(
                self.pokemon_add,
                args=[poketeam.id]
            ),
            payload
        )

        assert res.status_code == status.HTTP_200_OK

    def test_add_pokemon_not_of_my_team(
        self,
        client_log,
        user_log,
        other_user_log,
        pokemon_factory,
        poketeam_factory
    ):
        """
        Test that is not possible to add a pokemon of another
        trainer in my team
        """
        # Create a pokemon with a trainer "macha"
        pokemon = pokemon_factory(
            trainer=other_user_log
        )

        # Create a poketeam with a trainer "tai"
        poketeam = poketeam_factory(
            trainer=user_log
        )

        payload = {
            "pokemon": pokemon.id
        }
        expected_res = {
            "detail": "You do not have permission to perform this action."
        }

        # Try to add the pokemon of macha into the team of tai
        res = client_log.patch(
            reverse(
                self.pokemon_add,
                args=[poketeam.id]
            ),
            payload
        )

        assert res.status_code == status.HTTP_403_FORBIDDEN
        assert res.data == expected_res

    def test_remove_pokemon_from_a_team(
        self,
        user_log,
        client_log,
        poketeam_factory,
        pokemon_factory
    ):
        """
        Add a pokemon to a team then try to remove it
        """
        # Create the poketeam
        poketeam = poketeam_factory(
            trainer=user_log
        )
        # Create a pokemon with the same trainer and attached to the poketeam
        pokemon = pokemon_factory(
            trainer=user_log,
            team=poketeam
        )
        assert pokemon.team == poketeam

        # Try to remove pokemon from the team
        payload = {
            "pokemon": pokemon.id
        }

        res = client_log.patch(
            reverse(
                self.pokemon_remove,
                args=[poketeam.id]
            ),
            payload
        )

        assert res.status_code == status.HTTP_200_OK
