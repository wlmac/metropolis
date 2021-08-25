from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

router = SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('announcements/feed', AnnouncementListMyFeed.as_view(), name='announcement_feed'),
    path('announcements', AnnouncementListAll.as_view(), name='all_announcements'),
    path('clubs', OrganizationList.as_view(), name='list_clubs'),
    path('club/<int:pk>', OrganizationDetail.as_view(), name='club_detail'),
    path('events', EventsList.as_view(), name='event_list'),
    path('timetables', TimetableList.as_view(), name='timetable_list'),
    path('timetable/<int:pk>/today', TimetableToday.as_view(), name='timetable_today'),
    path('timetable/<int:pk>', TimetableDetails.as_view(), name='timetable_detail'),
]
