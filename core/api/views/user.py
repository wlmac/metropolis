from .. import serializers
from .. import utils
from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from ... import models
from rest_framework.response import Response
import datetime


class UserDetail(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'

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
        ongoing_timetables = request.user.get_ongoing_timetables()

        if len(ongoing_timetables) == 0:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        elif len(ongoing_timetables) >= 2:
            return Response({'detail': 'Misconfigured Terms: Contact Admin'}, status=500)

        serializer = serializers.TimetableSerializer(ongoing_timetables[0])
        return Response(serializer.data)
