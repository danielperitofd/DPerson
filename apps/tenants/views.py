from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from apps.accounts.forms import TenantUserForm
from apps.core.mixins import MasterRequiredMixin

from .forms import TenantForm
from .models import Tenant, TenantMembership
from .services import delete_test_data, get_seed_profiles, get_seed_status, populate_test_data

User = get_user_model()


class TenantListView(MasterRequiredMixin, ListView):
    model = Tenant
    template_name = "tenants/tenant_list.html"
    context_object_name = "tenants"


class TenantCreateView(MasterRequiredMixin, CreateView):
    model = Tenant
    form_class = TenantForm
    template_name = "tenants/tenant_form.html"
    success_url = reverse_lazy("tenants:list")

    def form_valid(self, form):
        messages.success(self.request, "Tenant criada com sucesso.")
        return super().form_valid(form)


class TenantUpdateView(MasterRequiredMixin, UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name = "tenants/tenant_form.html"
    success_url = reverse_lazy("tenants:list")

    def form_valid(self, form):
        messages.success(self.request, "Tenant atualizada com sucesso.")
        return super().form_valid(form)


class TenantDeleteView(MasterRequiredMixin, DeleteView):
    model = Tenant
    template_name = "shared/confirm_delete.html"
    success_url = reverse_lazy("tenants:list")

    def form_valid(self, form):
        messages.success(self.request, "Tenant removida com sucesso.")
        return super().form_valid(form)


class TenantSeedControlView(MasterRequiredMixin, TemplateView):
    template_name = "tenants/seed_control.html"

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        profile_key = request.POST.get("profile")
        profiles = get_seed_profiles()
        if action == "populate":
            if profile_key not in profiles:
                messages.error(request, "Perfil de seed invalido.")
            else:
                result = populate_test_data(profile_key)
                messages.success(
                    request,
                    f"Perfil {result['profile_label']} criado: tenant {result['tenant'].name}, aluno {result['student'].full_name}, {result['assessment_count']} avaliacoes fisicas. Admin: {result['accounts']['admin_username']} | Staff: {result['accounts']['staff_username']} | Senha: {result['accounts']['password']}",
                )
        elif action == "delete":
            result = delete_test_data(profile_key or None)
            if result["tenants_deleted"]:
                messages.success(request, f"Seeds removidos com sucesso. Tenants excluidas: {result['tenants_deleted']}. Usuarios excluidos: {result['users_deleted']}.")
            else:
                messages.info(request, "Nao havia dados seed para excluir.")
        return redirect("tenants:seed_control")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "seed_profiles": get_seed_status(),
            }
        )
        return context


class TenantTeamListView(MasterRequiredMixin, ListView):
    template_name = "tenants/tenant_team_list.html"
    context_object_name = "memberships"

    def dispatch(self, request, *args, **kwargs):
        self.tenant = get_object_or_404(Tenant, pk=self.kwargs["tenant_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.tenant.memberships.select_related("user").order_by("role", "user__full_name", "user__username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["managed_tenant"] = self.tenant
        return context


class TenantTeamCreateView(MasterRequiredMixin, CreateView):
    model = User
    form_class = TenantUserForm
    template_name = "tenants/tenant_team_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.tenant = get_object_or_404(Tenant, pk=self.kwargs["tenant_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("tenants:team_list", kwargs={"tenant_pk": self.tenant.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["managed_tenant"] = self.tenant
        return context

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        membership_role = form.cleaned_data["membership_role"]
        has_default = TenantMembership.objects.filter(tenant=self.tenant, is_default=True).exists()
        TenantMembership.objects.update_or_create(
            tenant=self.tenant,
            user=self.object,
            defaults={
                "role": membership_role,
                "is_active": self.object.is_active,
                "is_default": not has_default,
            },
        )
        if membership_role == TenantMembership.Role.ADMIN:
            self.tenant.primary_admin = self.object
            self.tenant.save(update_fields=["primary_admin"])
        messages.success(self.request, "Usuario provisionado na tenant com sucesso.")
        return response


class TenantTeamUpdateView(MasterRequiredMixin, UpdateView):
    model = User
    form_class = TenantUserForm
    template_name = "tenants/tenant_team_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.tenant = get_object_or_404(Tenant, pk=self.kwargs["tenant_pk"])
        self.membership = get_object_or_404(TenantMembership.objects.select_related("user"), pk=self.kwargs["membership_pk"], tenant=self.tenant)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.membership.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["membership"] = self.membership
        return kwargs

    def get_success_url(self):
        return reverse("tenants:team_list", kwargs={"tenant_pk": self.tenant.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["managed_tenant"] = self.tenant
        return context

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        self.membership.role = form.cleaned_data["membership_role"]
        self.membership.is_active = self.object.is_active
        self.membership.save(update_fields=["role", "is_active", "updated_at"])
        if self.membership.role == TenantMembership.Role.ADMIN:
            self.tenant.primary_admin = self.object
            self.tenant.save(update_fields=["primary_admin"])
        elif self.tenant.primary_admin_id == self.object.id:
            replacement = self.tenant.memberships.filter(role=TenantMembership.Role.ADMIN, is_active=True).exclude(pk=self.membership.pk).first()
            self.tenant.primary_admin = replacement.user if replacement else None
            self.tenant.save(update_fields=["primary_admin"])
        messages.success(self.request, "Usuario da tenant atualizado com sucesso.")
        return response


class TenantTeamDeleteView(MasterRequiredMixin, DeleteView):
    model = TenantMembership
    template_name = "shared/confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        self.tenant = get_object_or_404(Tenant, pk=self.kwargs["tenant_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return TenantMembership.objects.filter(tenant=self.tenant).select_related("user")

    def get_success_url(self):
        return reverse("tenants:team_list", kwargs={"tenant_pk": self.tenant.pk})

    @transaction.atomic
    def form_valid(self, form):
        membership = self.get_object()
        membership.is_active = False
        membership.user.is_active = False
        membership.user.save(update_fields=["is_active"])
        membership.save(update_fields=["is_active", "updated_at"])
        if self.tenant.primary_admin_id == membership.user_id:
            replacement = self.tenant.memberships.filter(role=TenantMembership.Role.ADMIN, is_active=True).exclude(pk=membership.pk).first()
            self.tenant.primary_admin = replacement.user if replacement else None
            self.tenant.save(update_fields=["primary_admin"])
        messages.success(self.request, "Usuario da tenant desativado com sucesso.")
        return HttpResponseRedirect(self.get_success_url())
