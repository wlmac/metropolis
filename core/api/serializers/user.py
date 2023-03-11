from rest_framework import serializers

from ... import models
from .tag import TagSerializer
from ...templatetags.gravatar_tags import gravatar_url


class UserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Tag.objects.all())
    organizations = serializers.SlugRelatedField(
        slug_field="name", many=True, queryset=models.Organization.objects.all()
    )
    tags_following = TagSerializer(many=True)

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "timezone",
            "graduating_year",
            "organizations",
            "tags_following",
        ]


class UserSerializerInternal(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Tag.objects.all())

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "is_superuser",
            "date_joined",
            "bio",
            "timezone",
            "graduating_year",
            "is_teacher",
            "organizations",
            "tags_following",
            "qltrs",
        ]


class UserSerializer3(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Tag.objects.all())
    gravatar_url = serializers.SerializerMethodField(read_only=True)

    def get_gravatar_url(self, obj):
        return gravatar_url(obj.email)

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "bio",
            "timezone",
            "graduating_year",
            "organizations",
            "tags_following",
            "gravatar_url",
        ]
