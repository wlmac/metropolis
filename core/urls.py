from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from . import views
from .api.views import MartorImageUpload
from .utils.sitemaps import *

urlpatterns = [
    path(
        "martor/api/upload-image/",
        MartorImageUpload.as_view(),
        name="api_martor_image_upload",
    ),
    path("", views.Index.as_view(), name="index"),
    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": {
                "blog": BlogSitemap,
                "announcements": AnnouncementsSitemap,
                "clubs": ClubsSitemap,
            }
        },
        name="django.contrib.sitemaps.views.sitemaps",
    ),
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
    path(
        "announcement/<int:pk>",
        views.AnnouncementDetail.as_view(),
        name="announcement_detail",
    ),
    path(
        "announcements/tag/<int:tag>",
        views.AnnouncementTagList.as_view(),
        name="announcement_tag_list",
    ),
    path("announcements/feed", views.AnnouncementFeed(), name="announcement_feed"),
    path("gallery", views.ExhibitList.as_view(), name="exhibit_list"),
    path("blog", views.BlogPostList.as_view(), name="blogpost_list"),
    path("blog/<str:slug>", views.BlogPostDetail.as_view(), name="blogpost_detail"),
    path(
        "blog/tag/<int:tag>", views.BlogPostTagList.as_view(), name="blogpost_tag_list"
    ),
    path("calendar", views.CalendarView.as_view(), name="calendar"),
    path("calendar.ics", views.CalendarFeed(), name="calendar_ical"),
    path("map", views.MapView.as_view(), name="map"),
    path("about", views.AboutView.as_view(), name="about"),
    path("teapot", views.Teapot.as_view(), name="teapot"),
    path("justinian", views.Justinian.as_view(), name="justinian"),
    path("json", views.Json.as_view(), name="json"),
    path("tv", views.TVView.as_view(), name="tv"),
    path("tv/clubs", views.TVClubView.as_view(), name="tvclub"),
    path("c/<int:pk>", views.OrganizationShort.as_view(), name="organization_short"),
    path("raffle", views.RaffleRedirect.as_view(), name="raffle"),
    path("hijack/", include("hijack.urls")),
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
