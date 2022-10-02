from rest_framework import generics


class ListAPIViewWithFallback(generics.ListAPIView):
    def get(self, request): # fixme Signature of method 'ListAPIViewWithFallback.get()' does not match signature of the base method in class 'ListAPIView'
        if len(set(request.query_params) & {"limit", "offset"}) == 0:
            self.pagination_class = None
        return super().get(request)
