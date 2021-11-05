import os
import uuid
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import authentication, exceptions, parsers, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.file_upload import file_upload_path_generator


class MartorImageUpload(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {
                    "status": 400,
                    "error": "You are currently unauthorized to upload images. Please contact an administrator.",
                }
            )

        if "markdown-image-upload" not in request.FILES:
            return Response({"status": 400, "error": "Missing image file."})

        image = request.FILES["markdown-image-upload"]

        ext = os.path.splitext(image.name)[1]

        if ext not in settings.MARTOR_UPLOAD_SAFE_EXTS:
            return Response({"status": 400, "error": "Invalid image format."})

        file_path = default_storage.save(
            file_upload_path_generator(settings.MARTOR_UPLOAD_MEDIA_DIR)(
                image, image.name
            ),
            image,
        )

        image_url = urljoin(settings.MEDIA_URL, file_path)

        return Response({"status": 200, "name": "", "link": image_url})
