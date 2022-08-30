import datetime

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ... import models
from ... import utils as utils2
from .. import serializers, utils
from ..utils import ListAPIViewWithFallback


class TermList(ListAPIViewWithFallback):
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

        return Response(
            {
                target_date.isoformat(): term.day_schedule(target_date=target_date)
                for target_date in [
                    date + datetime.timedelta(days=days) for days in range(7)
                ]
            }
        )


class TermCurrent(APIView):
    def get(self, request, format=None):
        term = models.Term.get_current()

        if term is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.TermSerializer(term)
        return Response(serializer.data)


class TermCurrentSchedule(APIView):
    def get(self, request, format=None):
        term = models.Term.get_current()
        date = utils.parse_date_query_param(request)

        if term is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        return Response(term.day_schedule(target_date=date))
