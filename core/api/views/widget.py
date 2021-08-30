from rest_framework import authentication, permissions, parsers, status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import default_storage
import uuid
import os
from metropolis import settings
from urllib.parse import urljoin


class MartorImageUpload(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

    def post(self, request):
        if 'markdown-image-upload' not in request.FILES:
            return Response({'status': 400, 'error': 'Missing image file.'})

        image = request.FILES['markdown-image-upload']

        file_name, ext = os.path.splitext(image.name)
        
        if ext not in settings.MARTOR_UPLOAD_SAFE_EXTS:
            return Response({'status': 400, 'error': 'Invalid image format.'})

        file_name = uuid.uuid4().hex

        file_path = default_storage.save(os.path.join(settings.MARTOR_UPLOAD_MEDIA_DIR, file_name + ext), image)
        
        image_url = urljoin(settings.MEDIA_URL, file_path)

        return Response({'status': 200, 'name': '', 'link': image_url})
