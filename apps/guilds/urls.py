from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.guilds.views import GuildViewSet

router = DefaultRouter()
router.register(r'guilds', GuildViewSet, basename='guild')

urlpatterns = [
    path('', include(router.urls)),
]
