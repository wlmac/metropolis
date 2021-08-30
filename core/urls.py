from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('api/', include('core.api.urls')),
    path('timetable', views.TimetableList.as_view(), name='timetable_list'),
    path('timetable/add/term/<int:pk>', views.TimetableCreate.as_view(), name='timetable_create'),
    path('timetable/edit/<int:pk>', views.TimetableUpdate.as_view(), name='timetable_update'),
    path('course/add/term/<int:pk>', views.CourseCreate.as_view(), name='course_create'),
    path('accounts/profile', views.ProfileRedirect.as_view(), name='profile_redirect'),
    path('accounts/profile/update', views.ProfileUpdate.as_view(), name='profile_update'),
    path('user/<str:slug>', views.Profile.as_view(), name='profile_detail'),
    path('clubs', views.OrganizationList.as_view(), name='organization_list'),
    path('club/<str:slug>', views.OrganizationDetail.as_view(), name='organization_detail'),
    path('announcements', views.AnnouncementList.as_view(), name='announcement_list'),
    path('calendar', views.calendar, name="calendar")
]
