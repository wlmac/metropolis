from .. import serializers
from .. import utils
from rest_framework import generics, permissions
from rest_framework.views import APIView
from ... import models
from rest_framework.response import Response
from metropolis.settings import TIMETABLE_FORMATS
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
import datetime


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
