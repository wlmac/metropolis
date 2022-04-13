from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


from ... import models
from .. import serializers



class ProveAccess(APIView):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["prove_access"]
    parser_classes = [JSONParser]

    def get(self, request, format=None):
        if 'nonce' not in request.data.keys():
            return Response(
                {'error': 'missing nonce'},
                status=400
            )
        nonce = request.data['nonce']
        return Response({'proof': proof})
