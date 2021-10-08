from rest_framework import serializers


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
