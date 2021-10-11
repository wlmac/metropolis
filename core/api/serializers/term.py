from rest_framework import serializers

from ... import models


class TermSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Term.objects.all())

    class Meta:
        model = models.Term
        fields = "__all__"
