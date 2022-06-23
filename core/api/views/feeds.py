from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

__ALL__ = ['feeds']

@api_view()
def feeds(request):
    return Response(list(settings.ANNOUNCEMENTS_CUSTOM_FEEDS))
