from django.urls import path

from .views import SaaSLoginView, SaaSLogoutView, TenantUserCreateView, TenantUserDeleteView, TenantUserListView, TenantUserUpdateView

app_name = "accounts"

urlpatterns = [
    path("login/", SaaSLoginView.as_view(), name="login"),
    path("logout/", SaaSLogoutView.as_view(), name="logout"),
    path("usuarios/", TenantUserListView.as_view(), name="tenant_user_list"),
    path("usuarios/novo/", TenantUserCreateView.as_view(), name="tenant_user_create"),
    path("usuarios/<int:membership_pk>/editar/", TenantUserUpdateView.as_view(), name="tenant_user_update"),
    path("usuarios/<int:pk>/excluir/", TenantUserDeleteView.as_view(), name="tenant_user_delete"),
]
