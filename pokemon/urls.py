from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PokemonViewSet
from .views import FavObjectViewSet
app_name = "pokemon"

router = DefaultRouter()
router.register("", PokemonViewSet, basename="pokemon")
# router.register("object", FavObjectViewSet, basename="favobject") list and retrieve with search doesn't work


urlpatterns = [
    path("", include(router.urls)),
    path("object/<int:pk>",
         FavObjectViewSet.as_view({'get': 'retrieve'}), name='favobject-id'),
]
