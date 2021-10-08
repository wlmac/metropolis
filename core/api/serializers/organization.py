from rest_framework import serializers

from core.api.serializers.custom import PrimaryKeyAndSlugRelatedField

from ... import models
from .tag import TagSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    owner = PrimaryKeyAndSlugRelatedField(
        slug_field="username", queryset=models.User.objects.all()
    )
    supervisors = PrimaryKeyAndSlugRelatedField(
        slug_field="username", many=True, queryset=models.User.objects.all()
    )
    execs = PrimaryKeyAndSlugRelatedField(
        slug_field="username", many=True, queryset=models.User.objects.all()
    )

    tags = TagSerializer(many=True)

    class Meta:
        model = models.Organization
        fields = "__all__"
