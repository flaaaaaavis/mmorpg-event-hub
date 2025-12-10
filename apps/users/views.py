from rest_framework import viewsets

from apps.users.models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o CRUD completo de Users.

    Operações suportadas:
    - list, retrieve, create, update, partial_update, destroy
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
