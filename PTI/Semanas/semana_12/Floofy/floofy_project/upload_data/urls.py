from django.urls import path
from . import views

urlpatterns = [
    path('years/', views.upload_years, name='upload-years'),
    path('degrees/', views.upload_degrees, name='upload-degrees'),
    path('subjects/', views.upload_subjects, name='upload-subjects'),
    path('blocks/', views.upload_blocks, name='upload-blocks'),
    path('students/', views.upload_students, name='upload-students'),
    path('teachers/', views.upload_teachers, name='upload-teachers'),
    path('groups/', views.upload_groups, name='upload-groups'),
    path('tasks/', views.upload_tasks, name='upload-tasks'),
    path('stages/', views.upload_stages, name='upload-stages'),
    path('meetings/', views.upload_meetings, name='upload-meetings'),
    path('feedback/', views.upload_feedback, name='upload-feedback'),
    path('', views.upload_area, name='upload-area'),
]
