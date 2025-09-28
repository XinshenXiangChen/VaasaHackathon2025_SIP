from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('api/upload/', views.api_upload_csv, name='api_upload_csv'),
    path('api/data/', views.api_get_data, name='api_get_data'),
    path('visualization/', views.visualization, name='visualization'),
]