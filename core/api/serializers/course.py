from rest_framework import serializers

from ... import models
from .organization import OrganizationSerializer
from .tag import TagSerializer


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Term
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(min_value=1, max_value=4)

    class Meta:
        model = models.Course
        fields = ["id", "code", "description", "position"]


class EventSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Event
        exclude = ["schedule_format", "is_instructional"]
