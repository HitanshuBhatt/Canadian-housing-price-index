from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # home page 
    path("charts/", views.charts, name="charts"), # charts page 
    path("upload/", views.upload_csv, name="upload_csv"), # upload page
]