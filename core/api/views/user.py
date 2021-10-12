import datetime

from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ... import models
from .. import serializers, utils


class UserDetail(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "username"


class UserMe(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)


class UserMeSchedule(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        date = utils.parse_date_query_param(request)

        return Response(request.user.schedule(target_date=date))


class UserMeScheduleWeek(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        date = utils.parse_date_query_param(request)

        result = {}

        for day in range(7):
            result[date.isoformat()] = request.user.schedule(target_date=date)
            date += datetime.timedelta(days=1)

        return Response(result)


class UserMeTimetable(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        current_timetable = request.user.get_current_timetable()

        if current_timetable is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.TimetableSerializer(current_timetable)
        return Response(serializer.data)
