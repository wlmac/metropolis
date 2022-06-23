from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

__ALL__ = ['feeds']

@api_view()
def feeds(request):
    """
    Returns Announcement feeds.

    https://noi.nyiyui.ca/k/1063/5041#Get_Feeds
    """
    return Response(list(settings.ANNOUNCEMENTS_CUSTOM_FEEDS))
