from .. import serializers
from rest_framework import generics, permissions
from rest_framework.views import APIView
from ... import models
from rest_framework.response import Response
from metropolis.settings import TIMETABLE_FORMATS
from rest_framework import status


class TimetableList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        timetables = models.Timetable.objects.filter(owner=request.user)
        serializer = serializers.TimetableSerializer(timetables, many=True)
        return Response(serializer.data)


class TimetableToday(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        timetable = models.Timetable.objects.get(pk=pk)

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

        for i in timetable_config['schedule']:
            course = i['position'][day-1].intersection(set(courses.keys())).pop()
            response['schedule'].append({
                'info': i['info'],
                'course': courses[course].code
            })

        return Response(response)


class TimetableDetails(generics.RetrieveAPIView):
    queryset = models.Timetable.objects.all()
    serializer_class = serializers.TimetableSerializer
