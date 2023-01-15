from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PokemonViewSet
from .views import FavObjectViewSet


router = DefaultRouter()
router.register("pokemon", PokemonViewSet, basename="pokemon")
router.register("favobject", FavObjectViewSet, basename="favobject")


urlpatterns = [
    path("", include(router.urls)),
]
