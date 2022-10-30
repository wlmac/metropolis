from django.conf import settings
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("api/", include("core.api.urls")),
    path("timetable", views.TimetableList.as_view(), name="timetable_list"),
    path(
        "timetable/add/term/<int:pk>",
        views.TimetableCreate.as_view(),
        name="timetable_create",
    ),
    path(
        "timetable/edit/<int:pk>",
        views.TimetableUpdate.as_view(),
        name="timetable_update",
    ),
    path(
        "course/add/term/<int:pk>", views.CourseCreate.as_view(), name="course_create"
    ),
    path("accounts/profile", views.ProfileRedirect.as_view(), name="profile_redirect"),
    path(
        "accounts/profile/update", views.ProfileUpdate.as_view(), name="profile_update"
    ),
    path("user/<str:slug>", views.Profile.as_view(), name="profile_detail"),
    path("clubs", views.OrganizationList.as_view(), name="organization_list"),
    path(
        "club/<str:slug>",
        views.OrganizationDetail.as_view(),
        name="organization_detail",
    ),
    path("announcements", views.AnnouncementList.as_view(), name="announcement_list"),
    path("announcements/feed", views.AnnouncementFeed(), name="announcement_feed"),
    path(
        "announcement/<int:pk>",
        views.AnnouncementDetail.as_view(),
        name="announcement_detail",
    ),
    path("blog", views.BlogPostList.as_view(), name="blogpost_list"),
    path("blog/<str:slug>", views.BlogPostDetail.as_view(), name="blogpost_detail"),
    path("calendar", views.CalendarView.as_view(), name="calendar"),
    path("calendar.ics", views.CalendarFeed(), name="calendar_ical"),
    path("map", views.MapView.as_view(), name="map"),
    path("about", views.AboutView.as_view(), name="about"),
    path("teapot", views.Teapot.as_view(), name="teapot"),
    path("justinian", views.Justinian.as_view(), name="justinian"),
    path("tv", views.TVView.as_view(), name="tv"),
    path("tv/clubs", views.TVClubView.as_view(), name="tvclub"),
    path("c/<int:pk>", views.OrganizationShort.as_view(), name="organization_short"),
    path("raffle", views.RaffleRedirect.as_view(), name="raffle"),
]

if settings.LAZY_LOADING:
    urlpatterns += [
        path(
            "announcements/cards",
            views.AnnouncementCards.as_view(),
            name="api_announcements_card",
        ),
        path(
            "blogs/cards",
            views.BlogPostCards.as_view(),
            name="api_blog_card",
        ),
    ]
