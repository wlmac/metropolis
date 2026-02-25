from rest_framework import serializers

from ... import models
from .organization import OrganizationSerializer
from .tag import TagSerializer


class EventSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Event
        exclude = ["schedule_format", "is_instructional"]
