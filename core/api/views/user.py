import datetime

from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import serializers, utils
from ... import models

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import api_view
from core.models import User
from core.api.serializers.user import UserSerializer

@extend_schema(
    responses={200: UserSerializer(many=True)},
)
@api_view(["GET"])
def userDetail(request, year=None):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "username__iexact"
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["user"]

@extend_schema(
    responses={200: UserSerializer(many=True)},
)
@api_view(["GET"])
def userMe(request, year=None):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_meta"]

    def get(self, request, format=None):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)

@extend_schema(
    responses={200: UserSerializer(many=True)},
)
@api_view(["GET"])
def userMeInternal(request, year=None):
    permission_classes = [TokenHasScope]
    required_scopes = ["me_meta", "internal"]

    def get(self, request, format=None):
        serializer = serializers.UserSerializerInternal(request.user)
        return Response(serializer.data)

@extend_schema(
    responses={200: UserSerializer(many=True)},
)
@api_view(["GET"])
def userMeSchedule(request, year=None):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_schedule"]

    def get(self, request, format=None):
        date = utils.parse_date_query_param(request)

        return Response(request.user.schedule(target_date=date))

@extend_schema(
    responses={200: UserSerializer(many=True)},
)
@api_view(["GET"])
def userMeScheduleWeek(request, year=None):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_schedule"]

    def get(self, request, format=None):
        date = utils.parse_date_query_param(request)

        return Response(
            {
                target_date.isoformat(): request.user.schedule(target_date=target_date)
                for target_date in [
                    date + datetime.timedelta(days=days) for days in range(7)
                ]
            }
        )

@extend_schema(
    responses={200: UserSerializer(many=True)},
)
@api_view(["GET"])
def userMeTimetable(request, year=None):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_timetable"]

    def get(self, request, format=None):
        current_timetable = request.user.get_current_timetable()

        if current_timetable is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.TimetableSerializer(current_timetable)
        return Response(serializer.data)
