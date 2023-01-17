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
        expected_return = {
            "id": 2,
            "name": "Test poketeam",
            "pokemon": [
                {
                    "id": 1,
                    "pokedex_creature": 1,
                    "trainer": 2,
                    "nickname": "Creature 1",
                    "level": 1,
                    "experience": 0,
                    "favorite_object": 1
                }
            ]
        }
        assert res.status_code == status.HTTP_200_OK
        assert res.data == expected_return

    def test_create_poketeam(
        self,
        user_log,
        client_log,
    ):
        """
        Create a new poketeam and confirm the team is attached to the client_log
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
        assert res.data== expected_return
