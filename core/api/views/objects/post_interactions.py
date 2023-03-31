from __future__ import annotations

from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import permissions, serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

from .base import BaseProvider
from ...utils.posts import likes, comments
from ....models import Comment, User, Like

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


class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    edited = serializers.SerializerMethodField(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.filter(id__in=[18, 21, 16]),
        many=False
        # 16 = Announcement, 18 = Blogpost, 21 = Comment
    )

    def validate(self, attrs):
        """
        https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
        """
        if self.context["request"].user.is_anonymous:
            raise serializers.ValidationError("You must be logged in to comment.")
        if parent := attrs.get("parent", None):
            id = attrs.get("id", None)
            if parent.id == id:
                raise ValidationError("A Comment cannot be a parent of itself.")

        return super().validate(attrs)

    def get_author(self, obj: Comment) -> User | None:
        if obj.author is not None:
            return obj.author.id
        return None

    def get_likes(self, obj: Comment) -> int:
        return likes(obj)

    def get_children(self, obj: Comment):
        return comments(self.context, obj, replies=True)

    @staticmethod
    def get_edited(obj: Comment):
        return obj.last_modified != obj.created_at

    def update(self, instance: Comment, validated_data) -> Comment:
        if instance.deleted:
            raise ValidationError("This comment has been deleted.")
        if instance.body != validated_data.get(
            "body", instance.body
        ):  # if change is  to body.
            instance.last_modified = timezone.now()
        super().update(instance, validated_data)
        return instance

    @staticmethod
    def delete(instance: Comment):
        instance.delete(force=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    class Meta:
        model = Comment
        permissions = [IsOwnerOrSuperuser]
        fields = [
            "id",
            "author",
            "content_type",
            "object_id",
            "body",
            "created_at",
            "likes",
            "edited",
            "children",
        ]


class CommentNewSerializer(CommentSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data) -> Comment:
        com = Comment(**validated_data)
        if validated_data["author"].is_superuser:  # bypass moderation if user is staff.
            com.live = True
        com.save()
        return com

    class Meta:
        model = Comment
        permission_classes = [IsAuthenticated]
        fields = [
            "content_type",
            "object_id",  # obj id of the blogpost or announcement.
            "body",
            "parent",
            "author",
        ]


class CommentProvider(BaseProvider):
    """
    TODO:
    - add the profanity check on comment creation.
    """
    model = Comment
    allow_list = False
    allow_new = settings.ALLOW_COMMENTS

    @property
    def permission_classes(self):
        return [permissions.IsAuthenticated]

    @property
    def serializer_class(self):
        return dict(
            new=CommentNewSerializer,
        ).get(self.request.kind, CommentSerializer)

    def get_queryset(self, request):
        if (
            request.user.has_perm("core.comment.view_flagged")
            or request.user.is_superuser
        ):
            return Comment.objects.all()
        return Comment.objects.filter(live=True)

    def get_last_modified(self, view):
        return view.get_object().last_modified_date

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="comment")
            )
            .latest("action_time")
            .action_time
        )


# ====================================================================================================
# -------------------------------------------  LIKES  -------------------------------------------
# ====================================================================================================


class LikeSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.filter(id__in=[18, 21, 16]),
        many=False
        # 16 = Announcement, 18 = Blogpost, 21 = Comment
    )

    def create(self, validated_data) -> Like:
        VALID_OBJECT_TYPES = ["Announcement", "Blogpost", "Comment"]
        obj_name = validated_data["content_type"].name.capitalize().replace(" ", "")
        if (
            not validated_data["content_type"]
            .model_class()  # the model of the content type ( e.g. core.models.Announcement or core.models.Comment )
            .objects.filter(id=validated_data["object_id"])
            .exists()
        ):  # does the object exist?
            raise ValidationError(f"The specified {obj_name} does not exist.")
        elif obj_name not in VALID_OBJECT_TYPES:  # is the object type valid?
            raise ValidationError(
                f"Invalid object type: {obj_name}, valid types are: {VALID_OBJECT_TYPES}"
            )
        elif Like.objects.filter(  # has the user already liked this object?
            content_type=validated_data["content_type"],
            object_id=validated_data["object_id"],
            author=validated_data["author"],
        ).exists():
            raise ValidationError(f"User has already liked this {obj_name}")
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

    @property
    def permission_classes(self):
        return [permissions.IsAuthenticated]

    def get_queryset(self, request):
        return Like.objects.all()

    @property
    def serializer_class(self):
        return LikeSerializer

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
