import uuid
from django.db import models
from apps.users.models import User
from apps.guilds.models import Guild

# Create your models here.
class Player(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    awards = models.JSONField(default=list)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="players")
    guild = models.ForeignKey(Guild, on_delete=models.SET_NULL, null=True, blank=True, related_name="players")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Player {self.id}"
