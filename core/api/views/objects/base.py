from typing import List, Literal


class BaseProvider:
    allow_list: bool = (
        True  # Is the view able to list the model's objects. (e.g. /user would list all users
    )
    allow_new: bool = True  # Is the provider able to create a new object.
    kind: Literal["list", "new", "single", "retrieve"]  # type of view
    listing_filters_ignore: List[str] = []
    # ^ don't treat the passed in params as a listing filter but instead as a param for the view.

    def __init__(self, request):
        self.request = request
