class BaseProvider:
    allow_list = True
    allow_new = True
    kind = ""

    def __init__(self, request):
        self.request = request
