from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

router = SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('announcements/feed', AnnouncementListMyFeed.as_view(), name='api_announcement_feed'),
    path('announcements', AnnouncementListAll.as_view(), name='api_all_announcements'),
    path('organizations', OrganizationList.as_view(), name='api_organization_list'),
    path('organization/<int:pk>', OrganizationDetail.as_view(), name='api_organization_detail'),
    path('user/<str:username>', UserDetail.as_view(), name='api_user_detail'),
    path('me', UserMe.as_view(), name='api_me'),
    path('me/schedule', UserMeSchedule.as_view(), name='api_me_schedule'),
    path('me/timetable', UserMeTimetable.as_view(), name='api_me_timetable'),
    path('events', EventsList.as_view(), name='api_event_list'),
    path('timetables', TimetableList.as_view(), name='api_timetable_list'),
    path('timetable/<int:pk>/schedule', TimetableSchedule.as_view(), name='api_timetable_schedule'),
    path('timetable/<int:pk>', TimetableDetails.as_view(), name='api_timetable_detail'),
    path('martor/upload-image', MartorImageUpload.as_view(), name='api_martor_image_upload'),
    path('version', APIVersion.as_view(), name='api_version'),
]
