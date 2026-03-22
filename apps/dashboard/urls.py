from django.urls import path

from .views import DashboardHomeView, MasterControlCenterView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardHomeView.as_view(), name="home"),
    path("control-center/", MasterControlCenterView.as_view(), name="control_center"),
]
