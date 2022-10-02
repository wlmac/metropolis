from rest_framework import generics


class ListAPIViewWithFallback(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        if len(set(request.query_params) & {"limit", "offset"}) == 0:
            self.pagination_class = None
        return super().get(request, *args, **kwargs)
