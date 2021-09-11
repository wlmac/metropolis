from .. import serializers
from rest_framework import generics, permissions
from rest_framework.views import APIView
from ... import models
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .. import utils
import datetime


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
