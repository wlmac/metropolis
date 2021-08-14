from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('timetable/add', views.AddTimetableSelectTerm.as_view(), name='add_timetable_select_term'),
    path('timetable/add/term/<int:pk>', views.AddTimetableSelectCourses.as_view(), name='add_timetable_select_courses'),
    path('timetable/view/<int:pk>', views.ViewTimetable.as_view(), name='view_timetable'),
    path('timetable/view/<int:pk>/data', views.ViewTimetableData.as_view(), name='view_timetable_data'),
    path('course/add/term/<int:pk>', views.AddCourse.as_view(), name='add_course'),
    path('accounts/profile', views.ProfileRedirect.as_view(), name='profile_redirect'),
    path('accounts/profile/update', views.ProfileUpdate.as_view(), name='profile_update'),
    path('user/<str:slug>', views.Profile.as_view(), name='profile_detail'),
    path('clubs', views.OrganizationList.as_view(), name='organization_list'),
    path('club/<int:pk>', views.OrganizationDetail.as_view(), name='organization_detail'),
    path('news', views.AnnouncementList.as_view(), name='announcement_list'),
]
