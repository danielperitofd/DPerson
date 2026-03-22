from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import TenantPermissionRequiredMixin
from apps.core.permissions import TenantPermissions
from apps.tenants.models import TenantMembership

from .forms import LoginForm, TenantUserForm

User = get_user_model()


class SaaSLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class SaaSLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


class TenantUserListView(TenantPermissionRequiredMixin, ListView):
    template_name = "accounts/user_list.html"
    context_object_name = "memberships"
    required_tenant_permission = TenantPermissions.USERS

    def get_queryset(self):
        return TenantMembership.objects.filter(tenant=self.request.active_tenant).select_related("user", "tenant").order_by("role", "user__full_name", "user__username")


class TenantUserCreateView(TenantPermissionRequiredMixin, CreateView):
    model = User
    form_class = TenantUserForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("accounts:tenant_user_list")
    required_tenant_permission = TenantPermissions.USERS

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        has_default = TenantMembership.objects.filter(tenant=self.request.active_tenant, is_default=True).exists()
        TenantMembership.objects.update_or_create(
            tenant=self.request.active_tenant,
            user=self.object,
            defaults={
                "role": form.cleaned_data["membership_role"],
                "is_active": True,
                "is_default": not has_default,
            },
        )
        messages.success(self.request, "Usuario da tenant criado com sucesso.")
        return response


class TenantUserUpdateView(TenantPermissionRequiredMixin, UpdateView):
    model = User
    form_class = TenantUserForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("accounts:tenant_user_list")
    required_tenant_permission = TenantPermissions.USERS

    def dispatch(self, request, *args, **kwargs):
        self.membership = TenantMembership.objects.filter(pk=self.kwargs["membership_pk"], tenant=request.active_tenant).select_related("user").first()
        if self.membership is None:
            return HttpResponseRedirect(reverse_lazy("accounts:tenant_user_list"))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.membership.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["membership"] = self.membership
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        self.membership.role = form.cleaned_data["membership_role"]
        self.membership.is_active = self.object.is_active
        self.membership.save(update_fields=["role", "is_active", "updated_at"])
        messages.success(self.request, "Usuario da tenant atualizado com sucesso.")
        return response


class TenantUserDeleteView(TenantPermissionRequiredMixin, DeleteView):
    model = TenantMembership
    template_name = "shared/confirm_delete.html"
    success_url = reverse_lazy("accounts:tenant_user_list")
    required_tenant_permission = TenantPermissions.USERS

    def get_queryset(self):
        return TenantMembership.objects.filter(tenant=self.request.active_tenant).select_related("user")

    @transaction.atomic
    def form_valid(self, form):
        membership = self.get_object()
        if membership.user == self.request.user:
            messages.error(self.request, "Voce nao pode remover o proprio acesso por esta tela.")
            return HttpResponseRedirect(self.get_success_url())
        membership.is_active = False
        membership.user.is_active = False
        membership.user.save(update_fields=["is_active"])
        membership.save(update_fields=["is_active", "updated_at"])
        messages.success(self.request, "Usuario da tenant desativado com sucesso.")
        return HttpResponseRedirect(self.get_success_url())
