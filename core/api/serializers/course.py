from rest_framework import serializers
from ... import models


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Term
        fields = [
            'name',
            'description',
            'timetable_format',
            'start_date',
            'end_date',
            'is_frozen'
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = [
            'code',
            'term',
            'description',
            'position'
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = [
            'name',
            'term',
            'description',
            'start_date',
            'end_date',
            'is_instructional'
        ]
