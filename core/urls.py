from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('timetable/add', views.AddTimetableSelectTerm.as_view(), name='add_timetable_select_term'),
    path('timetable/add/term/<int:pk>', views.AddTimetableSelectCourses.as_view(), name='add_timetable_select_courses'),
    path('timetable/view/<int:pk>', views.ViewTimetable.as_view(), name='view_timetable'),
    path('timetable/view/<int:pk>/data', views.ViewTimetableData.as_view(), name='view_timetable_data'),
    path('course/view/<int:pk>', views.ViewCourse.as_view(), name='view_course'),
    path('course/add/term/<int:pk>', views.AddCourse.as_view(), name='add_course'),
    path('accounts/profile', views.ProfileRedirect.as_view(), name='profile_redirect'),
    path('accounts/school', views.SchoolRedirect.as_view(), name='school_redirect'),
    path('accounts/profile/update', views.ProfileUpdate.as_view(), name='profile_update'),
    path('user/<str:slug>', views.Profile.as_view(), name='profile_detail'),
    path('school/<int:pk>', views.ViewSchool.as_view(), name='view_school'),
    path('school/<int:pk>/data', views.ViewSchoolData.as_view(), name='view_school_data'),
    path('term/<int:pk>', views.ViewTerm.as_view(), name='view_term'),
    path('term/<int:pk>/data', views.ViewTermData.as_view(), name='view_term_data'),
    path('event/<int:pk>/data', views.ViewEventData.as_view(), name='view_event_data'),
]
