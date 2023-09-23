from django.urls import path
from .views import views

urlpatterns = [
    path("use_case", views.add_use_case),
    path("list_simulators", views.list_simulators),
    path("restart_simulator", views.restart_simulator),
    path("stop_simulator", views.stop_simulator),
    path("check_status", views.check_status),
]
