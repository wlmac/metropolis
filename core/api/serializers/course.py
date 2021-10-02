from rest_framework import serializers

from .tag import TagSerializer
from ... import models


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Term
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(slug_field='name', queryset=models.Organization.objects.all())
    organization_id = serializers.PrimaryKeyRelatedField(queryset=models.Organization.objects.all())
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Event
        exclude = ['schedule_format', 'is_instructional']
