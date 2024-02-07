"""metropolis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import FileResponse
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_page
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularAPIView,
    SpectacularRedocView,
)
from oauth2_provider.urls import base_urlpatterns, app_name
from pwa.views import manifest, offline


def service_worker(request):
    return FileResponse(
        open(settings.PWA_SERVICE_WORKER_PATH, "rb"),
        content_type="application/javascript",
    )


pwa_urlpatterns = [
    re_path(r"^serviceworker\.js$", service_worker, name="serviceworker"),
    # overwrite django pwa's default service worker view to fix mem leak
    re_path(r"^manifest\.json$", manifest, name="manifest"),
    re_path("^offline/$", offline, name="offline"),
]

urlpatterns = [
    path("", include("core.urls")),
    path("", include((base_urlpatterns, app_name), namespace=app_name)),
    path("", include(pwa_urlpatterns)),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("martor/", include("martor.urls")),
    path("select2/", include("django_select2.urls")),
    path("<path:url>", include("django.contrib.flatpages.urls")),
    path("docs", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "api/schema/", cache_page(60 * 30)(SpectacularAPIView.as_view()), name="schema"
    ),  # cache for 30m
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
