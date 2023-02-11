from rest_framework import serializers

from core.api.serializers.custom import PrimaryKeyAndSlugRelatedField

from ... import models
from .course import CourseSerializer, TermSerializer


class TimetableSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Tag.objects.all())
    owner = PrimaryKeyAndSlugRelatedField(
        slug_field="username", queryset=models.User.objects.all()
    )
    term = TermSerializer()
    courses = CourseSerializer(many=True)

    class Meta:
        model = models.Timetable
        fields = "__all__"
