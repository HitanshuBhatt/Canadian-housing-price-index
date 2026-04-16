from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.charts, name='charts'),
=======
>>>>>>> ccd8006370106471d8c992d922fb9bd8ba3a989e
    path('upload/', views.upload_csv, name='upload_csv'),
]