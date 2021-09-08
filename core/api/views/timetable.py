from .. import serializers
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


class TimetableToday(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        timetable = get_object_or_404(models.Timetable, pk=pk)

        if request.user != timetable.owner:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        timetable_format = timetable.term.timetable_format
        timetable_config = TIMETABLE_FORMATS[timetable_format]
        day = timetable.term.day()
        courses = {}
        for i in timetable.courses.all():
            courses[i.position] = i

        response = {
            'timetable': serializers.TimetableSerializer(timetable).data,
            'schedule': []
        }

        if day is None:
            response['schedule'] = None
            return Response(response)

        for i in timetable_config['schedules'][timetable.term.day_schedule()]:
            course = i['position'][day-1].intersection(set(courses.keys())).pop()

            start_time = timezone.make_aware(datetime.datetime.combine(timezone.localdate(), datetime.time(*i['time'][0], 0)))
            end_time = timezone.make_aware(datetime.datetime.combine(timezone.localdate(), datetime.time(*i['time'][1], 0)))

            response['schedule'].append({
                'description': i['description'],
                'time': {
                    'start': start_time,
                    'end': end_time,
                },
                'course': courses[course].code,
            })

        return Response(response)


class TimetableDetails(generics.RetrieveAPIView):
    permission_classes = [IsOwner]
    queryset = models.Timetable.objects.all()
    serializer_class = serializers.TimetableSerializer
