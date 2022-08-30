from rest_framework import generics


class ListAPIViewWithFallback(generics.ListAPIView):
    def get(self, request):
        if len(set(request.query_params) & set(["limit", "offset"])) == 0:
            self.pagination_class = None
        return super().get(request)
