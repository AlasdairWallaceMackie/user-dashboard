from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('admin', views.dashboard_admin, name="dashboard_admin"),
]