from django.utils import timezone
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import serializers
from ... import models


class EventsList(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    def get(self, request):
        start = timezone.now()
        if request.data.get('start'):
            start = request.data.get('start')
        if request.data.get('end'):
            end = request.data.get('end')
            events = models.Event.objects.filter(end_date__gte=start, end_date__lte=end).order_by('start_date')
        else:
            events = models.Event.objects.filter(end_date__gte=start).order_by('start_date')

        serializer = serializers.EventSerializer(events, many=True)
        return Response(serializer.data)