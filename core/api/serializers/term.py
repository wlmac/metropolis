from rest_framework import serializers
from .tag import TagSerializer
from ... import models


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Term
        fields = '__all__'
