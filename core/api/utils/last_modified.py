from rest_framework import generics

class GenericAPIViewWithLastModified(generics.GenericAPIView):
    def get_last_modified(self):
        raise NotImplemented()

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        resp["Last-Modified"] = self.get_last_modified()
        return resp
