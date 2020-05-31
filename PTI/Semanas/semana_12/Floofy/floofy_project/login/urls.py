from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.log_in, name='login-home'),
    path('logged-student/', views.loggedstudent, name='logged-student'),
    path('logged-teacher/', views.loggedteacher, name='logged-teacher'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/monday/', views.monday, name='monday'),
    path('schedule/tuesday/', views.tuesday, name='tuesday'),
    path('schedule/wednesday/', views.wednesday, name='wednesday'),
    path('schedule/thursday/', views.thursday, name='thursday'),
    path('schedule/friday/', views.friday, name='friday'),
    path('subjectpage/', views.select_subject_page, name='select-subject-page'),
    path('pastsubjectpage/', views.select_past_subject_page, name='select-past-subject-page'),
    path('subject/<int:sub_id>/', views.subject_page, name='subject-page'),
    path('myprofile/', views.my_profile, name='my-profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login/logout.html'), name='logout')
]