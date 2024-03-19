from rest_framework import serializers

from core.api.serializers.custom import PrimaryKeyAndSlugRelatedField
from core.api.serializers.tag import TagSerializer

from ... import models


class AnnouncementSerializer(serializers.ModelSerializer):
    author = PrimaryKeyAndSlugRelatedField(
        slug_field="username", queryset=models.User.objects.all()
    )
    organization = PrimaryKeyAndSlugRelatedField(
        slug_field="slug", queryset=models.Organization.objects.all()
    )
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Announcement
        exclude = ["supervisor", "status", "rejection_reason"]
