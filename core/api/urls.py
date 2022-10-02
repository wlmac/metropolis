from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *
from .views.objects import *

router = SimpleRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token", TokenObtainPairView.as_view(), name="api_token_obtain_pair"),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="api_token_refresh"),
    path("notifications/new", NotificationsNew.as_view(), name="api_notification_new"),
    path(
        "announcements/feed",
        AnnouncementListMyFeed.as_view(),
        name="api_announcement_feed",
    ),
    path("announcements", AnnouncementListAll.as_view(), name="api_all_announcements"),
    path(
        "announcements/changes",
        AnnouncementChangeStream.as_view(),
        name="api_announcement_changes",
    ),
    path("organizations", OrganizationList.as_view(), name="api_organization_list"),
    path(
        "organization/<int:pk>",
        OrganizationDetail.as_view(),
        name="api_organization_detail",
    ),
    path("user/<str:username>", UserDetail.as_view(), name="api_user_detail"),
    path("v3/user/<int:id>", UserDetail3.as_view(), name="api_user_detail3"),
    path("me", UserMe.as_view(), name="api_me"),
    path("me/schedule", UserMeSchedule.as_view(), name="api_me_schedule"),
    path("me/schedule/week", UserMeScheduleWeek.as_view(), name="api_me_schedule_week"),
    path("me/timetable", UserMeTimetable.as_view(), name="api_me_timetable"),
    path("events", EventsList.as_view(), name="api_event_list"),
    path("timetables", TimetableList.as_view(), name="api_timetable_list"),
    path(
        "timetable/<int:pk>/schedule",
        TimetableSchedule.as_view(),
        name="api_timetable_schedule",
    ),
    path("timetable/<int:pk>", TimetableDetails.as_view(), name="api_timetable_detail"),
    path("terms", TermList.as_view(), name="api_term_list"),
    path("term/<int:pk>", TermDetail.as_view(), name="api_term_detail"),
    path("term/current", TermCurrent.as_view(), name="api_term_current"),
    path("term/<int:pk>/schedule", TermSchedule.as_view(), name="api_term_schedule"),
    path(
        "term/current/schedule", TermCurrentSchedule.as_view(), name="api_term_schedule"
    ),
    path(
        "term/<int:pk>/schedule/week",
        TermScheduleWeek.as_view(),
        name="api_term_schedule_week",
    ),
    path(
        "martor/upload-image",
        MartorImageUpload.as_view(),
        name="api_martor_image_upload",
    ),
    path("v3/staff", staff, name="api_staff3"),
    path("v3/feeds", feeds, name="api_feeds3"),
    path("v3/obj/<str:type>", ObjectList.as_view(), name="api_object_list3"),
    path("v3/obj/<str:type>/new", ObjectNew.as_view(), name="api_object_new3"),
    path("v3/obj/<str:type>/single/<path:id>", ObjectSingle.as_view(), name="api_object_single3"),
    path("v3/obj/<str:type>/retrieve/<path:id>", ObjectRetrieve.as_view(), name="api_object_retrieve3"),
    path("version", APIVersion.as_view(), name="api_version"),
]
