from django.urls import path

from .views import (
    TenantCreateView,
    TenantDeleteView,
    TenantListView,
    TenantSeedControlView,
    TenantTeamCreateView,
    TenantTeamDeleteView,
    TenantTeamListView,
    TenantTeamUpdateView,
    TenantUpdateView,
)

app_name = "tenants"

urlpatterns = [
    path("", TenantListView.as_view(), name="list"),
    path("popular-test/", TenantSeedControlView.as_view(), name="seed_control"),
    path("novo/", TenantCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", TenantUpdateView.as_view(), name="update"),
    path("<int:pk>/excluir/", TenantDeleteView.as_view(), name="delete"),
    path("<int:tenant_pk>/equipe/", TenantTeamListView.as_view(), name="team_list"),
    path("<int:tenant_pk>/equipe/novo/", TenantTeamCreateView.as_view(), name="team_create"),
    path("<int:tenant_pk>/equipe/<int:membership_pk>/editar/", TenantTeamUpdateView.as_view(), name="team_update"),
    path("<int:tenant_pk>/equipe/<int:pk>/excluir/", TenantTeamDeleteView.as_view(), name="team_delete"),
]
