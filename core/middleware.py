import pytz
from django.utils import timezone

from django.conf import settings


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            timezone.activate(pytz.timezone(request.user.timezone))
        else:
            timezone.activate(pytz.timezone(settings.DEFAULT_TIMEZONE))
        return self.get_response(request)
