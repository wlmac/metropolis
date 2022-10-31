from rest_framework import generics, serializers
from wsgiref.handlers import format_date_time
from time import mktime


class GenericAPIViewWithLastModified():
    def get_last_modified(self):
        raise NotImplemented()

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        resp["Last-Modified"] = format_date_time(mktime(self.get_last_modified().timetuple()))
        return resp


class GenericAPIViewWithDebugInfo(generics.GenericAPIView):
    def get_admin_url(self):
        return None

    def get_as_su(self):
        return False

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        if admin_url := self.get_admin_url():
            resp["X-Admin-URL"] = admin_url
        if self.get_as_su():
            resp["X-As-SU"] = 'true'

        return resp


class ModelAbilityField(serializers.ModelField):
    def __init__(self, ability, *args, **kwargs):
        self.ability = ability
        super().__init__(*args, **kwargs)

    def get_attribute(self, instance):
        return super().get_attribute(instance) if self.check(instance) else None

    def check(self, instance):
        user = self.context['request'].user
        key = f'can_{self.ability}'
        if not hasattr(user, key):
            return False
        if getattr(user, key)(instance) or user.is_superuser:
            return True
        return False


class PrimaryKeyRelatedAbilityField(serializers.PrimaryKeyRelatedField):
    def __init__(self, ability, *args, **kwargs):
        self.ability = ability
        super().__init__(*args, **kwargs)

    def get_attribute(self, instance):
        return super().get_attribute(instance) if self.check(instance) else None

    def check(self, instance):
        user = self.context['request'].user
        key = f'can_{self.ability}'
        if not hasattr(user, key):
            return False
        if getattr(user, key)(instance) or user.is_superuser:
            return True
        return False
