from rest_framework import serializers
from ... import models
from .course import TermSerializer, CourseSerializer


class TimetableSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    owner = serializers.SlugRelatedField(slug_field='username', queryset=models.User.objects.all())
    term = TermSerializer()
    courses = CourseSerializer(many=True)