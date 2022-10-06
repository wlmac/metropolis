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
