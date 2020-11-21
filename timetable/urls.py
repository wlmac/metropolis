from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('timetable/add', views.AddTimetable.as_view(), name='add_timetable'),
    path('timetable/view/<int:pk>', views.ViewTimetable.as_view(), name='view_timetable'),
    path('course/<int:pk>/term/<int:term>', views.ViewCourse.as_view(), name='view_course'),
    path('accounts/profile', views.ProfileRedirect.as_view(), name='profile_redirect'),
    path('accounts/school', views.SchoolRedirect.as_view(), name='school_redirect'),
    path('accounts/profile/update', views.ProfileUpdate.as_view(), name='profile_update'),
    path('user/<str:slug>', views.Profile.as_view(), name='profile_detail'),
    path('school/<int:pk>', views.ViewSchool.as_view(), name='view_school'),
]
