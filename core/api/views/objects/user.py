import base64
import hashlib

from django.conf import settings
from django.utils import timezone
from rest_framework import permissions, serializers, validators

from .base import BaseProvider
from .... import models
from ....models import User


class Serializer(serializers.ModelSerializer):
    email_hash = serializers.SerializerMethodField(read_only=True)

    def get_email_hash(self, obj):
        return base64.standard_b64encode(
            hashlib.md5(obj.email.encode("utf-8")).digest()
        )

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


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "graduating_year",
        ]


def tdsb_email(value):
    if not (
        value.endswith(settings.TEACHER_EMAIL_SUFFIX)
        and value.endswith(settings.STUDENT_EMAIL_SUFFIX)
    ):
        raise serializers.ValidationError("Must be either a teacher or student email.")


class NewSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    graduating_year = serializers.ChoiceField(
        choices=models.graduating_year_choices, required=True
    )
    email = serializers.EmailField(
        validators=[
            tdsb_email,
            validators.UniqueValidator(queryset=models.User.objects.all()),
        ],
        required=True,
    )
    username = serializers.RegexField(
        "^[\w.@+-]+$",
        validators=[validators.UniqueValidator(queryset=models.User.objects.all())],
        max_length=30,
        required=True,
    )
    password = serializers.CharField(required=True)

    # Default `create` and `update` behavior...
    def create(self, validated_data):
        user = User()
        keys = [
            "first_name",
            "last_name",
            "graduating_year",
            "email",
            "username",
            "password",
        ]
        for key in keys:
            setattr(user, key, validated_data[key])
        if validated_data["email"].endswith(settings.TEACHER_EMAIL_SUFFIX):
            user.is_teacher = True
        user.save()
        return instance  # fixme instance is not defined

    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "graduating_year",
            "email",
            "username",
            "password",
            "bio",
            "timezone",
            "organizations",
            "tags_following",
        ]


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
        return dict(
            new=NewSerializer,
            list=ListSerializer,
        ).get(self.request.kind, Serializer)

    def get_queryset(self, request):
        return models.User.objects.filter(is_active=True)

    def get_last_modified(self, view):
        return timezone.now()

    def get_last_modified_queryset(self):
        return timezone.now()
