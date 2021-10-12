from rest_framework import serializers

from ... import models


class TagSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Tag.objects.all())

    class Meta:
        model = models.Tag
        fields = ["id", "name", "color"]
