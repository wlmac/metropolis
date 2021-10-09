from rest_framework import serializers

from core.api.serializers.custom import PrimaryKeyAndSlugRelatedField
from .tag import TagSerializer
from .organization import OrganizationSerializer
from ... import models


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Term
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Event
        exclude = ["schedule_format", "is_instructional"]
