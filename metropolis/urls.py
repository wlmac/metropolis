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
from django.urls import include, path
from oauth2_provider.views import AuthorizationView, RevokeTokenView, TokenView
oauth2_endpoint_views = [
    path('authorize', AuthorizationView.as_view(), name="authorize"),
    path('token', TokenView.as_view(), name="token"),
    path('revoke-token', RevokeTokenView.as_view(), name="revoke-token"),
]

urlpatterns = [
    path("", include("core.urls")),
    path('o/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace="oauth2_provider")),
    path("", include("oauth2_provider.urls", "oauth2_provider"), namespace="oauth2_provider"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("martor/", include("martor.urls")),
    path("select2/", include("django_select2.urls")),
    path("", include("pwa.urls")),
    path("/<path:url>", include("django.contrib.flatpages.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
