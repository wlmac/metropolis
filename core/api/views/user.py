from django.shortcuts import get_object_or_404
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core import utils

from ... import models
from .. import serializers
from ..utils.parse_date import parse_date_query_param


class UserDetail(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "username"
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["user"]

    def get_object(self):
        username = self.kwargs.get(self.lookup_field)
        obj = get_object_or_404(self.queryset, username__iexact=username)
        return obj


class UserMe(APIView):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_meta"]

    @staticmethod
    def get(request, format=None):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)


class UserMeInternal(APIView):
    permission_classes = [TokenHasScope]
    required_scopes = ["me_meta", "internal"]

    @staticmethod
    def get(request, format=None):
        serializer = serializers.UserSerializerInternal(request.user)
        return Response(serializer.data)


class UserMeSchedule(APIView):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_schedule"]

    def get(self, request, format=None):
        date = parse_date_query_param(request)

        return Response(request.user.get_schedule(target_date=date))


class UserMeScheduleWeek(APIView):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_schedule"]

    @staticmethod
    def get(request, format=None):
        date = parse_date_query_param(request)

        return Response(utils.get_schedule.get_week_schedule(date, request.user))


class UserMeTimetable(APIView):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_timetable"]

    @staticmethod
    def get(request, format=None):
        timetable = request.user.get_timetable()

        if timetable is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.TimetableSerializer(timetable)
        return Response(serializer.data)
