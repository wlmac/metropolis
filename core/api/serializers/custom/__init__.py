from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from rest_framework import serializers
from rest_framework.fields import ChoiceField, Field, MultipleChoiceField

from core.api.utils.github import get_model_choices
from core.api.utils.gravatar import gravatar_url
from core.models import Comment, Organization, Tag, User


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
        choices = get_model_choices(
            model=ContentType,
            value_list=("model", self.slug_field),
            db_filter=dict(app_label="core", model__in=settings.POST_CONTENT_TYPES),
        )
        default_error_messages = {
            "does_not_exist": "ContentType with model '{value}' does not exist."
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


class SingleUserSerializer(serializers.ModelSerializer):
    gravatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "gravatar_url"]

    @staticmethod
    def get_gravatar_url(obj: User):
        return gravatar_url(obj.email)


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
            "liked": obj.likes.filter(author=self.context["request"].user).exists(),
        }


class CommentSerializer(serializers.ModelSerializer):
    author = SingleUserSerializer()
    has_children = serializers.SerializerMethodField(read_only=True)
    edited = serializers.SerializerMethodField(read_only=True)
    likes = LikeField()

    @staticmethod
    def get_edited(obj: Comment) -> bool:
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


class SingleUserField(ChoiceField):
    def __init__(self, **kwargs):
        self.slug_field = "username"
        choices = kwargs.get("choices", None) or get_model_choices(
            model=User,
            value_list=("id", self.slug_field),
            db_filter=dict(is_active=True),
        )

        default_error_messages = {"does_not_exist": "User '{value}' does not exist."}
        super().__init__(choices, **kwargs)
        self.default_error_messages.update(default_error_messages)

    def to_representation(self, value):
        return SingleUserSerializer(value).data if value else None

    def to_internal_value(self, data):
        try:
            return User.objects.get(id=data)
        except ObjectDoesNotExist:
            self.fail(
                "does_not_exist", slug_name=self.slug_field, value=smart_str(data)
            )
        except (TypeError, ValueError):
            self.fail("invalid")


class SupervisorField(SingleUserField):
    def __init__(self, *args, **kwargs):
        self.slug_field = "username"
        choices = get_model_choices(  # todo: fixme
            model=User,
            value_list=("id", self.slug_field),
            db_filter=dict(is_teacher=True, organizations_supervising__contains=[]),
        )
        kwargs["choices"] = choices
        super().__init__(**kwargs)


class MembersField(serializers.Field):
    def to_representation(self, value):
        return SingleUserSerializer(value, many=True).data

    def to_internal_value(self, data):
        if data is None:
            return None
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of user IDs.")

        users = User.objects.filter(id__in=data).values_list("id", flat=True)
        if len(users) != len(data):
            missing_ids = set(data) - set(users)
            for missing_id in missing_ids:
                self.fail(
                    "invalid", message=f"User with ID {missing_id} does not exist."
                )
        return User.objects.filter(id__in=data)

    @staticmethod
    def get_queryset():
        return User.objects.exclude(is_active=False)

    def __init__(self, **kwargs):
        default_error_messages = {
            "does_not_exist": "User with ID {value} does not exist.",
        }
        kwargs["help_text"] = "The User ID of the member of this object."
        super().__init__(**kwargs)
        self.default_error_messages.update(default_error_messages)


class OrganizationField(ChoiceField):
    def __init__(self, **kwargs):
        self.slug_field = "name"
        choices = get_model_choices(
            model=Organization,
            value_list=("id", self.slug_field),
            db_filter=dict(is_active=True),
        )
        default_error_messages = {
            "does_not_exist": "Organization '{value}' does not exist."
        }
        super().__init__(choices, **kwargs)
        self.default_error_messages.update(default_error_messages)

    def to_internal_value(self, data):
        try:
            return Organization.objects.get(pk=data)
        except ObjectDoesNotExist:
            self.fail(
                "does_not_exist", slug_name=self.slug_field, value=smart_str(data)
            )
        except (TypeError, ValueError):
            self.fail("invalid")

    def to_representation(self, obj):
        return OrganizationSerializer(obj).data if obj else None


class UserOrganizationField(OrganizationField):
    def to_representation(self, value):
        return OrganizationSerializer(value, many=True).data if value else None

    def to_internal_value(self, data):
        if data is None:
            return None
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of organization IDs.")

        organizations = Organization.objects.filter(id__in=data).values_list(
            "id", flat=True
        )
        if len(organizations) != len(data):
            missing_ids = set(data) - set(organizations)
            for missing_id in missing_ids:
                self.fail(
                    "invalid",
                    message=f"Organization with ID {missing_id} does not exist.",
                )
        return Organization.objects.filter(id__in=data)


class TagRelatedField(MultipleChoiceField):
    """
    A custom field to represent a list of Tag objects in the form of {id, name, color},
    but accepts input as a list of tag IDs.
    """

    def __init__(self, **kwargs):
        kwargs["required"] = False
        kwargs["choices"] = get_model_choices(model=Tag, value_list=("id", "name"))
        kwargs["help_text"] = "The Tags associated with this object."
        super().__init__(**kwargs)

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
