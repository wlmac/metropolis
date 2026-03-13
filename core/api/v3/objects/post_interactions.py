from __future__ import annotations

from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission, IsAuthenticated

from core.api.serializers.custom import (
    ContentTypeField,
)
from core.models import Like

from .base import BaseProvider

typedir: dict[str, str] = {
    "blogpost": "core | blogpost",
    "announcement": "core | announcements",
}


class IsOwnerOrSuperuser(BasePermission):
    """
    Allows access only to staff or the owner of the object.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_superuser
            or request.user == view.get_object().author
        )


# ====================================================================================================
# -------------------------------------------  LIKES  -------------------------------------------
# ====================================================================================================


class LikeSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField()

    def update(self, instance, validated_data):
        raise NotImplementedError(
            "You cannot update a like, if you wish to delete. do so."
        )

    def destroy(self, instance: Like, validated_data):
        if instance.author != self.context["request"].user:
            raise ValidationError("You cannot unlike another user's like.")
        instance.delete(force=True)

    def create(self, validated_data) -> Like:
        obj_name = validated_data["content_type"].name.lower().replace(" ", "")
        if (
            self.context["request"].user != validated_data["author"]
        ) and not self.context["request"].user.is_superuser:
            raise ValidationError("You cannot like as another user.")

        if obj_name not in settings.POST_CONTENT_TYPES:  # is the object type valid?
            raise ValidationError(
                f"Invalid object type: {obj_name}, valid types are: {settings.POST_CONTENT_TYPES}"
            )
        if (
            not validated_data["content_type"]
            .model_class()  # the model of the content type ( e.g. core.models.Announcement )
            .objects.filter(id=validated_data["object_id"])
            .exists()
        ):  # does the object exist?
            raise ValidationError(f"The specified {obj_name} does not exist.")

        if Like.objects.filter(  # has the user already liked this object?
            content_type=validated_data["content_type"],
            object_id=validated_data["object_id"],
            author=validated_data["author"],  # author is current user?
        ).exists():
            raise ValidationError(f"User has already liked this {obj_name}")
        else:
            like = Like(**validated_data)
            like.save()
            return like

    class Meta:
        model = Like
        permission_classes = [IsAuthenticated]
        fields = [
            "content_type",
            "object_id",  # obj id of the blogpost or announcement.
            "author",
        ]


class LikeProvider(BaseProvider):
    model = Like
    allow_list = False
    raw_serializers = {"_": LikeSerializer}

    @property
    def permission_classes(self):
        return [permissions.IsAuthenticated]

    def get_queryset(self, request):
        return Like.objects.all()

    def get_last_modified(self, view):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="like")
            )
            .filter(object_id=str(view.get_object().pk))
            .latest("action_time")
            .action_time
        )

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="like")
            )
            .latest("action_time")
            .action_time
        )
