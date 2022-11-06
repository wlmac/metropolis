import base64
import hashlib
from typing import List

from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import generics, permissions, validators
from rest_framework import serializers

from .... import models
from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    email_hash = serializers.SerializerMethodField(read_only=True)

    def get_email_hash(self, obj):
        return base64.standard_b64encode(hashlib.md5(obj.email.encode('utf-8')).digest())

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "email_hash",
            "first_name",
            "last_name",
            "bio",
            "timezone",
            "graduating_year",
            "organizations",
            "tags_following",
        ]


def tdsb_email(value):
    if not (validated_data["email"].endswith(settings.TEACHER_EMAIL_SUFFIX) and validated_data["email"].endswith(settings.STUDENT_EMAIL_SUFFIX)):
        raise serializers.ValidationError('Must be an allowed email.')



class NewSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    graduating_year = serializers.ChoiceField(choices=models.graduating_year_choices, required=True)
    email = serializers.EmailField(validators=[tdsb_email, validators.UniqueValidator(queryset=models.User.objects.all())], required=True)
    username = serializers.RegexField('^[\w.@+-]+$', validators=[validators.UniqueValidator(queryset=models.User.objects.all())], max_length=30, required=True)
    password = serializers.CharField(required=True)

    # Default `create` and `update` behavior...
    def create(self, validated_data):
        user = User()
        keys = ['first_name', 'last_name', 'graduating_year', 'email', 'username', 'password']
        for key in keys:
            setattr(user, key, validated_data[key])
        if validated_data["email"].endswith(settings.TEACHER_EMAIL_SUFFIX):
            user.is_teacher = True
        user.save()
        return instance

    class Meta:
        model = models.User
        fields = ["bio", "timezone", "organizations", "tags_following"]


class Identity(permissions.BasePermission):
    def has_object_permission(self, request, view, user):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == user:
            return True
        return False


class Provider(BaseProvider):
    model = models.User

    @property
    def permission_classes(self):
        return [Identity] if self.request.mutate else [permissions.IsAuthenticated]

    @property
    def serializer_class(self):
        if self.request.kind == 'new':
            return NewSerializer
        else:
            return Serializer

    def get_queryset(self, request):
        return models.User.objects.filter(is_active=True)

    def get_last_modified(self, view):
        return timezone.now()

    def get_last_modified_queryset(self):
        return timezone.now()
