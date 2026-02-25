from rest_framework import serializers

from core.api.serializers.custom import PrimaryKeyAndSlugRelatedField

from ... import models


class TimetableSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Tag.objects.all())
    owner = PrimaryKeyAndSlugRelatedField(
        slug_field="username", queryset=models.User.objects.all()
    )

    class Meta:
        model = models.Timetable
        fields = "__all__"
