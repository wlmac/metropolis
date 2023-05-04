from typing import List


class BaseProvider:
    allow_list: bool = True
    allow_new: bool = True
    kind: str = ""
    listing_filters_ignore: List[str] = []

    def __init__(self, request):
        self.request = request
