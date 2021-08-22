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


class EventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    description = serializers.CharField(allow_blank=True, style={'base_template': 'textarea.html'})
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    is_instructional = serializers.BooleanField(default=False)
    organization = serializers.SlugRelatedField(slug_field='name', queryset=models.Organization.objects.all(), required=False, allow_null=True, allow_empty=True)
    tags = serializers.SlugRelatedField(slug_field='name', many=True, queryset=models.Tag.objects.all())
