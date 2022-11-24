from django.db import models


class SetField(models.TextField):
    __token = " "

    def __init__(self, *args, **kwargs):
        super(SetField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return
        if isinstance(value, list):
            return value
        return value.split(self.__token)

    def get_db_prep_value(self, value, **kwargs):
        if not value:
            return
        assert isinstance(value, list) or isinstance(value, tuple)
        return self.__token.join(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
