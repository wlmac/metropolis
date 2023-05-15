from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from rest_framework import serializers
from rest_framework.fields import Field

from core.models import Tag, User, Organization, Comment


class PrimaryKeyAndSlugRelatedField(serializers.SlugRelatedField):
    def __init__(self, **kwargs):
        self.pk_field = kwargs.pop("pk_field", None)
        super().__init__(**kwargs)

    def to_representation(self, obj):
        if self.pk_field is not None:
            pk = self.pk_field.to_representation(obj.pk)
        else:
            pk = obj.pk
        return {
            "id": pk,
            "slug": getattr(obj, self.slug_field),
        }


class ContentTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        self.slug_field = "model"
        choices = ContentType.objects.filter(
            app_label="core", model__in=settings.POST_CONTENT_TYPES
        ).values_list("model", "model")
        default_error_messages = {
            "does_not_exist": "Organization with ID {value} does not exist."
        }
        super().__init__(choices, **kwargs)
        self.default_error_messages.update(default_error_messages)

    def to_internal_value(self, data):
        try:
            return ContentType.objects.get(app_label="core", model=data)
        except ObjectDoesNotExist:
            self.fail(
                "does_not_exist", slug_name=self.slug_field, value=smart_str(data)
            )
        except (TypeError, ValueError):
            self.fail("invalid")

    def to_representation(self, obj):
        return obj.model


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "slug", "icon"]


class LikeField(Field):
    def __init__(self, **kwargs):
        kwargs["read_only"] = True
        super().__init__(**kwargs)

    def to_representation(self, obj):
        return {
            "count": obj.likes.count(),
            "liked": obj.likes.filter(author=self.context["author"]).exists(),
        }


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    has_children = serializers.SerializerMethodField(read_only=True)
    edited = serializers.SerializerMethodField(read_only=True)
    likes = LikeField()

    @staticmethod
    def get_edited(obj: Comment):
        return obj.last_modified != obj.created_at

    @staticmethod
    def get_has_children(obj: Comment) -> bool:
        return obj.children.exists()

    class Meta:
        model = Comment
        fields = [
            "id",
            "body",
            "author",
            "has_children",
            "created_at",
            "edited",
            "likes",
        ]


class AuthorField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = User.objects.filter(is_staff=True).values_list("id", "username")
        default_error_messages = {
            "does_not_exist": "User with ID {value} does not exist.",
            "invalid": "Expected a int in the form of a User ID.",
        }
        super().__init__(choices, **kwargs)
        self.default_error_messages.update(default_error_messages)

    def to_representation(self, obj: User):
        return AuthorSerializer(obj).data

    def to_internal_value(self, data: int):
        if not (isinstance(data, int) or str(data).isdigit()):
            self.fail(
                "invalid",
            )
        try:
            return User.objects.get(id=data)
        except User.DoesNotExist:
            self.fail("does_not_exist", value=data)


class OrganizationField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = Organization.objects.filter(is_active=True).values_list("id", "name")
        default_error_messages = {
            "does_not_exist": "Organization with ID {value} does not exist.",
            "invalid": "Expected a int in the form of an Organization ID.",
        }
        super().__init__(choices, **kwargs)
        self.default_error_messages.update(default_error_messages)

    def to_representation(self, obj: User):
        return OrganizationSerializer(obj).data

    def to_internal_value(self, data: int):
        if not (isinstance(data, int) or str(data).isdigit()):
            self.fail("invalid")

        try:
            return Organization.objects.get(id=data)
        except Organization.DoesNotExist:
            self.fail("does_not_exist", value=data)


class TagRelatedField(serializers.MultipleChoiceField):
    """
    A custom field to represent a list of Tag objects in the form of {id, name, color},
    but accepts input as a list of tag IDs.
    """

    def __init__(self, **kwargs):
        kwargs["required"] = False
        choices = Tag.objects.all().values_list("id", "name")
        super().__init__(choices, **kwargs)

    def to_representation(self, value):
        """
        Convert the list of Tag objects to a list of {id, name, color} dictionaries.
        """
        return [
            {"id": tag.id, "name": tag.name, "color": tag.color} for tag in value.all()
        ]

    def to_internal_value(self, data):
        """
        Convert the list of tag IDs to a list of Tag objects.
        """
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tag IDs.")

        # Get the existing Tag objects.
        tags = Tag.objects.filter(id__in=data).values_list("id", flat=True)
        if len(tags) != len(data):
            missing_ids = set(data) - set(tags)
            for missing_id in missing_ids:
                self.fail(
                    "invalid", message=f"Tag with ID {missing_id} does not exist."
                )

        return Tag.objects.filter(id__in=data)


class CommentField(Field):
    def __init__(self, **kwargs):
        kwargs["read_only"] = True
        super().__init__(**kwargs)

    def to_representation(self, obj):
        return CommentSerializer(obj, many=True).data
