from .. import serializers
from rest_framework import generics, permissions
from rest_framework.views import APIView
from ... import models
from rest_framework.response import Response
from metropolis.settings import TIMETABLE_FORMATS


class TimetableList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        timetables = models.Timetable.objects.filter(owner=request.user)
        serializer = serializers.TimetableSerializer(timetables, many=True)
        return Response(serializer.data)


class TimetableToday(APIView):
    def get(self, request, pk):
        timetable = models.Timetable.objects.get(pk=pk)
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

        if not timetable.term.is_ongoing():
            response['schedule'] = None
            return Response(response)

        for i in timetable_config['schedule']:
            course = None
            for j in i['position'][day-1]:
                if j in courses.keys():
                    course = courses[j]
                    break
            response['schedule'].append({
                'info': i['info'],
                'course': course.code
            })

        return Response(response)