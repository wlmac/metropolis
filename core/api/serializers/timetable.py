from rest_framework import serializers
from ... import models
from .course import TermSerializer, CourseSerializer


class TimetableSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', queryset=models.User.objects.all())
    term = TermSerializer()
    courses = CourseSerializer(many=True)

    class Meta:
        model = models.Timetable
        fields = '__all__'
