class BaseProvider:
    allow_list = True
    allow_new = True

    def __init__(self, request):
        self.request = request
