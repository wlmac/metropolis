import pytz
from django.conf import settings
from django.contrib.redirects.middleware import RedirectFallbackMiddleware
from django.http import HttpResponseRedirect
from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            timezone.activate(pytz.timezone(request.user.timezone))
        else:
            timezone.activate(pytz.timezone(settings.DEFAULT_TIMEZONE))
        return self.get_response(request)


class RedirectFallbackTemporaryMiddleware(RedirectFallbackMiddleware):
    response_redirect_class = HttpResponseRedirect
