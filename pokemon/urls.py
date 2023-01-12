from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PokemonViewSet
from .views import FavObjectViewSet
app_name = "pokemon"

router = DefaultRouter()
router.register("", PokemonViewSet, basename="pokemon")


urlpatterns = [
    path("", include(router.urls)),
    path("favobjects/<int:pk>",
         FavObjectViewSet.as_view({'get': 'retrieve'}), name='favobject-id'),
    path("favobjects/<str:name>",
         FavObjectViewSet.as_view({'get': 'retrieve'}), name='favobject-name'),
    
]
