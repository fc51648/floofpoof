from django.urls import path
from . import views

urlpatterns = [
    path('years/', views.upload_years, name='upload-years'),
    path('degrees/', views.upload_degrees, name='upload-degrees'),
    path('subjects/', views.upload_subjects, name='upload-subjects'),
    path('blocks/', views.upload_blocks, name='upload-blocks'),
    path('', views.upload_area, name='upload-area'),
]
