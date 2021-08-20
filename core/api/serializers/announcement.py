from rest_framework import serializers
from ... import models


class AnnouncementSerializer(serializers.Serializer):
    author = serializers.SlugRelatedField(slug_field='username', allow_null=True)
    created_date = serializers.DateTimeField()
    last_modified_date = serializers.DateTimeField()

    title = serializers.CharField(max_length=128, allow_blank=True)
    body = serializers.CharField(allow_blank=True)
    tags = serializers.SlugRelatedField(slug_field='name', many=True)

    organization = serializers.SlugRelatedField(slug_field='name')

    is_public = serializers.BooleanField(default=True)
    supervisor = serializers.SlugRelatedField(slug_field='username', allow_empty=True, allow_null=True)
    status = serializers.ChoiceField(models.announcement_status_choices, default='p')
    rejection_reason = serializers.CharField(max_length=140, allow_blank=True)