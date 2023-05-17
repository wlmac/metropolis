import json

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


class ContentTypeField(serializers.Field):
    def __init__(self, **kwargs):
        default_error_messages = {
            "does_not_exist": "ContentType with model '{value}' does not exist.",
            "invalid": 'Invalid value. Expected string with the model name e.g. "Comment"',
        }
        kwargs["help_text"] = 'The model name e.g. "Comment" or "BlogPost"'
        super().__init__(**kwargs)
        self.default_error_messages.update(default_error_messages)

    def to_internal_value(self, data):
        try:
            return ContentType.objects.get(app_label="core", model=str(data).casefold())
        except ObjectDoesNotExist:
            self.fail("does_not_exist", value=smart_str(data))
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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "color"]


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


class AuthorField(serializers.Field):
    def to_representation(self, value):
        return AuthorSerializer(value).data if value else None

    def to_internal_value(self, data):
        if data is None:
            return None
        if isinstance(data, str):
            json_string_data = data.replace("'", '"')
            data = json.loads(json_string_data)
        if isinstance(data, dict):
            data = data.get("id")
        try:
            return User.objects.get(pk=data)
        except User.DoesNotExist:
            self.fail("does_not_exist", value=data)

    @staticmethod
    def get_queryset():
        return User.objects.exclude(is_active=False)

    def __init__(self, **kwargs):
        default_error_messages = {
            "does_not_exist": "User with ID {value} does not exist.",
        }
        kwargs["help_text"] = "The User ID of the author of this object."
        super().__init__(**kwargs)
        self.default_error_messages.update(default_error_messages)


class OrganizationField(serializers.Field):
    def to_representation(self, value):
        return OrganizationSerializer(value).data if value else None

    def to_internal_value(self, data):
        if data is None:
            return None
        if isinstance(data, str):
            json_string_data = data.replace("'", '"')
            data = json.loads(json_string_data)
        if isinstance(data, dict):
            data = data.get("id")
        try:
            return Organization.objects.get(pk=data)
        except Organization.DoesNotExist:
            self.fail("does_not_exist", value=data)

    @staticmethod
    def get_queryset():
        return Organization.objects.filter(is_active=True)

    def __init__(self, **kwargs):
        default_error_messages = {
            "does_not_exist": "Organization with ID {value} does not exist.",
        }
        kwargs["help_text"] = "The Organization ID of the org in charge of this object."
        super().__init__(**kwargs)
        self.default_error_messages.update(default_error_messages)


class TagRelatedField(serializers.MultipleChoiceField): # todo fix tests for this
    """
    A custom field to represent a list of Tag objects in the form of {id, name, color},
    but accepts input as a list of tag IDs.
    """

    def __init__(self, **kwargs):
        kwargs["required"] = False
        choices = Tag.objects.all().values_list("id", "name")
        kwargs["help_text"] = "The Tags associated with this object."
        super().__init__(choices, **kwargs)

    def to_representation(self, value):
        """
        Convert the list of Tag objects to a list of {id, name, color} dictionaries.
        """
        return TagSerializer(value, many=True).data

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
