from rest_framework import serializers

from core.models import Tag


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


class TagRelatedField(serializers.Field):
    """
    A custom field to represent a list of Tag objects in the form of {id, name, color},
    but accepts input as a list of tag IDs.
    """

    def __init__(self, **kwargs):
        kwargs["required"] = False
        super().__init__(**kwargs)

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
