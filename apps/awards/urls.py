from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.awards.views import AwardViewSet

router = DefaultRouter()
router.register(r'awards', AwardViewSet, basename='award')

urlpatterns = [
    path('', include(router.urls)),
]
