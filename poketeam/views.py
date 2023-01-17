from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Poketeam
from .serializers import PoketeamSerializer
from .serializers import PoketeamListSerializer
from .serializers import PoketeamDetailSerializer


class PoketeamViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PoketeamSerializer

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

    # @action(methods=['UPDATE'], detail=True, url_path="add-pokemon")
    # def add_pokemon(self, request, pk=None, pokemon_pk=None):
    #     pokemon = get_object_or_404(Pokemon, pk=pokemon_pk)
    #     team = get_object_or_404(Poketeam, pk=pk)
    #     serializer = self.serializer_class(
    #         team,
    #         data=request.data,
    #         partial=True
    #     )
    #     if serializer.is_valid():
    #         serializer.save(pokemon=pokemon)
    #         return Response(status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['UPDATE'], detail=True, url_path="remove-pokemon")
    # def remove_pokemon(self, request, pk=None):
    #    pass
