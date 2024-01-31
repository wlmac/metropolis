from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core import models
from core.models import User


class UserDeleteView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def post(self, id):
		user: User = User.objects.filter(id=id).first()
		if user is None:
			return Response(status=status.HTTP_410_GONE)
		elif user.is_deleted:
			return JsonResponse(
				status=status.HTTP_406_NOT_ACCEPTABLE,
				data={"error": "User is already deleted, Please use the restore endpoint."},
			)
		else:
			user.mark_deleted()
			return JsonResponse(status=status.HTTP_200_OK, data={"message": "User deleted."})


class UserRestoreView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def post(self, id):
		user: User = models.User.objects.filter(id=id).first()
		if user is None:
			return Response(status=status.HTTP_410_GONE)
		elif not user.is_deleted:
			return JsonResponse(
				status=status.HTTP_406_NOT_ACCEPTABLE,
				data={"error": "User is not marked for deletion, Please use the delete endpoint if you wish to delete your account."},
			)
		else:
			user.mark_restored()
			return Response(status=status.HTTP_200_OK)
