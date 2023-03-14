import datetime

from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import serializers, utils
from ..utils import GenericAPIViewWithLastModified, ListAPIViewWithFallback
from ... import models


class TermList(GenericAPIViewWithLastModified, ListAPIViewWithFallback):
    queryset = models.Term.objects.filter(
        end_date__gte=(timezone.now() - settings.TERM_GRACE_PERIOD)
    )
    serializer_class = serializers.TermSerializer

    def get_last_modified(self):
        # see https://docs.djangoproject.com/en/3.2/ref/contrib/admin/
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="term")
            )
            .latest("action_time")
            .action_time
        )


class TermDetail(generics.RetrieveAPIView):
    queryset = models.Term.objects.filter(
        end_date__gte=(timezone.now() - settings.TERM_GRACE_PERIOD)
    )
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
