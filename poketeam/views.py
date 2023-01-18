from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from pokemon.models import Pokemon

from .models import Poketeam
from .serializers import PoketeamSerializer
from .serializers import PoketeamListSerializer
from .serializers import PoketeamDetailSerializer
from .serializers import AddOrRemovePokemonFromTeamSerializer
from .permissions import PoketeamPermissions


class PoketeamViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PoketeamSerializer
    permission_classes = [PoketeamPermissions,]

    def get_queryset(self):
        qs = Poketeam.objects.filter(trainer=self.request.user.id)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return PoketeamListSerializer
        if self.action == 'retrieve':
            return PoketeamDetailSerializer

        return PoketeamSerializer

    def perform_create(self, serializer):
        return serializer.save(trainer=self.request.user)

    @action(methods=['PATCH'], detail=True,)
    def add_pokemon(self, request, pk=None):
        poketeam = self.get_object()
        serializer = AddOrRemovePokemonFromTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pokemon = Pokemon.objects.get(
            pk=serializer.validated_data['pokemon']
        )
        self.check_object_permissions(
            self.request,
            pokemon
        )
        pokemon.add_in_team(poketeam)
        pokemon.save()
        return Response(
            {
                "success":
                    f"the pokemon {pokemon} has been"
                    " added on the team {poketeam}",
            },
            status=status.HTTP_200_OK
        )

    @action(methods=['PATCH'], detail=True)
    def remove_pokemon(self, request, pk=None):
        poketeam = self.get_object()
        serializer = AddOrRemovePokemonFromTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pokemon = Pokemon.objects.get(
            pk=serializer.validated_data['pokemon']
        )
        self.check_object_permissions(
            self.request,
            pokemon
        )
        pokemon.remove_from_team(poketeam)
        pokemon.save()
        return Response(
            {
                "success":
                    f"the pokemon {pokemon} has been"
                    " removed from the team {poketeam}",
            },
            status=status.HTTP_200_OK
        )
