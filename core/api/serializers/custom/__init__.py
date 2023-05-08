from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from rest_framework import serializers

from core.models import Tag, User, Organization


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
        super().__init__(choices, **kwargs)

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


class AuthorField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = User.objects.filter(is_staff=True).values_list("id", "username")
        super().__init__(choices, **kwargs)

    def to_representation(self, obj: User):
        """
        Convert the list of Tag objects to a list of {id, name, color} dictionaries.
        """
        return AuthorSerializer(obj).data

    def to_internal_value(self, data: int):
        if not (isinstance(data, int) or str(data).isdigit()):
            raise serializers.ValidationError("Expected a int in the form of User ID.")

        # Get the existing User obj.
        try:
            user = User.objects.get(id=data)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User with ID {data} does not exist.")
        return user


class OrganizationField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = Organization.objects.filter(is_active=True).values_list("id", "name")
        super().__init__(choices, **kwargs)

    def to_representation(self, obj: User):
        """
        Convert the list of Tag objects to a list of {id, name, color} dictionaries.
        """
        return OrganizationSerializer(obj).data

    def to_internal_value(self, data: int):
        if not (isinstance(data, int) or str(data).isdigit()):
            raise serializers.ValidationError(
                "Expected a int in the form of Organization ID."
            )

        # Get the existing User obj.
        try:
            user = Organization.objects.get(id=data)
        except Tag.DoesNotExist:
            raise serializers.ValidationError(
                f"Organization with ID {data} does not exist."
            )
        return user


class TagRelatedField(serializers.MultipleChoiceField):
    """
    A custom field to represent a list of Tag objects in the form of {id, name, color},
    but accepts input as a list of tag IDs.
    """

    def __init__(self, **kwargs):
        kwargs["required"] = False
        if apps.get_model('core', 'tag'):
            choices = Tag.objects.all().values_list("id", "name")
        else:
            choices = []
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
        tags = []
        for tag_id in data:
            try:
                tag = Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                raise serializers.ValidationError(
                    f"Tag with ID {tag_id} does not exist."
                )
            tags.append(tag)

        return tags


# todo - add Comment and Like serializers.
