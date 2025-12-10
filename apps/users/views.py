from typing import Any
from rest_framework import viewsets
from django.db.models import QuerySet

from apps.users.models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet[Any]):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.all()