from rest_framework import generics
from wsgiref.handlers import format_date_time
from time import mktime


class GenericAPIViewWithLastModified(generics.GenericAPIView):
    def get_last_modified(self):
        raise NotImplemented()

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        resp["Last-Modified"] = format_date_time(mktime(self.get_last_modified().timetuple()))
        return resp
