from django.db.models import Q
from django.utils import timezone
from rest_framework import authentication, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication as jwt_auth

from ... import models
from .. import serializers


class EventsList(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    def get(self, request):
        start = timezone.now()
        if request.data.get("start"):
            start = request.data.get("start")
        elif request.query_params.get("start"):
            start = request.query_params.get("start")

        if not request.user.is_anonymous:
            if request.data.get("end"):
                end = request.data.get("end")
                events = (
                    models.Event.objects.filter(
                        end_date__gte=start, start_date__lte=end
                    )
                    .filter(Q(is_public=True) | Q(organization__member=request.user.id))
                    .distinct()
                    .order_by("start_date")
                )
            elif request.query_params.get("end"):
                end = request.query_params.get("end")
                events = (
                    models.Event.objects.filter(
                        end_date__gte=start, start_date__lte=end
                    )
                    .filter(Q(is_public=True) | Q(organization__member=request.user.id))
                    .distinct()
                    .order_by("start_date")
                )
            else:
                events = (
                    models.Event.objects.filter(end_date__gte=start)
                    .filter(Q(is_public=True) | Q(organization__member=request.user.id))
                    .distinct()
                    .order_by("start_date")
                )
        else:
            if request.data.get("end"):
                end = request.data.get("end")
                events = models.Event.objects.filter(
                    end_date__gte=start, start_date__lte=end, is_public=True
                ).order_by("start_date")
            elif request.query_params.get("end"):
                end = request.query_params.get("end")
                events = models.Event.objects.filter(
                    end_date__gte=start, start_date__lte=end, is_public=True
                ).order_by("start_date")
            else:
                events = models.Event.objects.filter(
                    end_date__gte=start, is_public=True
                ).order_by("start_date")

        serializer = serializers.EventSerializer(events, many=True)
        return Response(serializer.data)
