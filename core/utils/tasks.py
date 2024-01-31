"""
One off random tasks that need to be run on the server.
"""


import datetime as dt

from django.utils.crypto import get_random_string

from core.models import User


def get_random_username():
    """
    Generate a random username that is not already taken.
    """
    username = "deleted-" + get_random_string(length=6)
    if User.objects.filter(username=username).exists():
        return get_random_username()
    return username
