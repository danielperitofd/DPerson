from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from .permissions import user_has_tenant_permission


class MasterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class TenantAccessMixin(LoginRequiredMixin):
    tenant_field_name = "tenant"

    def ensure_tenant_access(self, request):
        if not request.user.is_superuser and request.active_tenant is None:
            messages.warning(request, "Selecione uma tenant ativa para continuar.")
            return redirect("dashboard:home")
        return None

    def dispatch(self, request, *args, **kwargs):
        redirect_response = self.ensure_tenant_access(request)
        if redirect_response is not None:
            return redirect_response
        return super().dispatch(request, *args, **kwargs)

    def get_tenant(self):
        return self.request.active_tenant

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.get_tenant() is None:
            return queryset.none()
        return queryset.filter(**{self.tenant_field_name: self.get_tenant()})

    def form_valid(self, form):
        tenant = self.get_tenant()
        if tenant and hasattr(form.instance, self.tenant_field_name + "_id"):
            setattr(form.instance, self.tenant_field_name, tenant)
        return super().form_valid(form)


class TenantPermissionRequiredMixin(TenantAccessMixin):
    required_tenant_permission = None

    def dispatch(self, request, *args, **kwargs):
        redirect_response = self.ensure_tenant_access(request)
        if redirect_response is not None:
            return redirect_response
        if self.required_tenant_permission and not user_has_tenant_permission(request.user, request.active_tenant, self.required_tenant_permission):
            raise PermissionDenied("Voce nao possui permissao para acessar esta area.")
        return super(TenantAccessMixin, self).dispatch(request, *args, **kwargs)


class TenantObjectPermissionMixin(TenantPermissionRequiredMixin):
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        tenant = self.get_tenant()
        tenant_value = getattr(obj, f"{self.tenant_field_name}_id", None)
        if tenant is None or tenant_value != tenant.id:
            raise PermissionDenied("Objeto fora da tenant ativa.")
        return obj
