from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("upload/", views.upload_csv, name="upload_csv"),
    path("charts/", views.charts, name="charts"),
]