class BaseProvider:
    allow_list = True
    def __init__(self, request):
        self.request = request
