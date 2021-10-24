import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ... import models
from .. import serializers, utils


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class TimetableList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        timetables = models.Timetable.objects.filter(owner=request.user)
        serializer = serializers.TimetableSerializer(timetables, many=True)
        return Response(serializer.data)


class TimetableSchedule(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        timetable = get_object_or_404(models.Timetable, pk=pk)

        if request.user != timetable.owner:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        date = utils.parse_date_query_param(request)

        return Response(timetable.day_schedule(target_date=date))


class TimetableDetails(generics.RetrieveAPIView):
    permission_classes = [IsOwner]
    queryset = models.Timetable.objects.all()
    serializer_class = serializers.TimetableSerializer
