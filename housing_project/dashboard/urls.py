from django.urls import path
from . import views

urlpatterns = [
    path('', views.charts, name='charts'),
    path('upload/', views.upload_csv, name='upload_csv'),
]