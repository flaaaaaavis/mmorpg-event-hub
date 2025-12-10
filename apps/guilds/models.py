import uuid
from django.db import models

# Create your models here.
class Guild(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=150)
    score = models.CharField(max_length=50)
    awards = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.name)
