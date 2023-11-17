from rest_framework import serializers

from core.api.serializers.custom import PrimaryKeyAndSlugRelatedField
from .tag import TagSerializer
from ... import models
from core.api.utils.gravatar import gravatar_url


class OrganizationSerializer(serializers.ModelSerializer):
    gravatar_url = serializers.SerializerMethodField(read_only=True)

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

    @staticmethod
    def get_gravatar_url(obj: models.Organization):
        return gravatar_url(obj.pk)
