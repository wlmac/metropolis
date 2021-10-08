import datetime

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ... import models
from .. import serializers, utils


class TermList(generics.ListAPIView):
    queryset = models.Term.objects.all()
    serializer_class = serializers.TermSerializer


class TermDetail(generics.RetrieveAPIView):
    queryset = models.Term.objects.all()
    serializer_class = serializers.TermSerializer


class TermSchedule(APIView):
    def get(self, request, pk, format=None):
        term = get_object_or_404(models.Term, pk=pk)
        date = utils.parse_date_query_param(request)

        return Response(term.day_schedule(target_date=date))


class TermScheduleWeek(APIView):
    def get(self, request, pk, format=None):
        term = get_object_or_404(models.Term, pk=pk)
        date = utils.parse_date_query_param(request)

        result = {}

        for day in range(7):
            result[date.isoformat()] = term.day_schedule(target_date=date)
            date += datetime.timedelta(days=1)

        return Response(result)


class TermCurrent(APIView):
    def get(self, request, format=None):
        term = models.Term.get_current()

        if term is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.TermSerializer(term)
        return Response(serializer.data)
