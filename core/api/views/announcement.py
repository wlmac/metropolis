from .. import serializers
from rest_framework import generics, permissions
from rest_framework.views import APIView
from ... import models
from django.db.models import Q
from rest_framework.response import Response

class AnnouncementListAll(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        announcements = models.Announcement.objects.filter(status='a').filter(is_public=True)
        serializer = serializers.AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)

class AnnouncementListMyFeed(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        announcements = models.Announcement.objects.filter(status='a').filter(Q(is_public=True, tags__follower=request.user) | Q(organization__member=request.user)).distinct()
        serializer = serializers.AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)