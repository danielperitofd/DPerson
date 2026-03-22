from django.urls import path

from .views import switch_tenant

app_name = "core"

urlpatterns = [
    path("switch/", switch_tenant, name="switch_tenant"),
]
