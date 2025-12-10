from typing import Any
from rest_framework import serializers
from apps.awards.models import Award


class AwardSerializer(serializers.ModelSerializer[Any]):
    class Meta:
        model = Award
        fields = "__all__"
        read_only_fields = ("id", "earned_at")
