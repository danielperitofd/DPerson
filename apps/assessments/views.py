from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import TenantObjectPermissionMixin, TenantPermissionRequiredMixin
from apps.core.permissions import TenantPermissions

from .forms import PhysicalAssessmentForm, PosturalAssessmentForm
from .models import PhysicalAssessment, PosturalAssessment


class PhysicalAssessmentListView(TenantPermissionRequiredMixin, ListView):
    model = PhysicalAssessment
    template_name = "assessments/physical_list.html"
    context_object_name = "assessments"
    paginate_by = 12
    required_tenant_permission = TenantPermissions.ASSESSMENTS


class PhysicalAssessmentCreateView(TenantPermissionRequiredMixin, CreateView):
    model = PhysicalAssessment
    form_class = PhysicalAssessmentForm
    template_name = "assessments/physical_form.html"
    success_url = reverse_lazy("assessments:physical_list")
    required_tenant_permission = TenantPermissions.ASSESSMENTS

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tenant"] = self.request.active_tenant
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Avaliacao fisica registrada com sucesso.")
        return super().form_valid(form)


class PhysicalAssessmentUpdateView(TenantObjectPermissionMixin, UpdateView):
    model = PhysicalAssessment
    form_class = PhysicalAssessmentForm
    template_name = "assessments/physical_form.html"
    success_url = reverse_lazy("assessments:physical_list")
    required_tenant_permission = TenantPermissions.ASSESSMENTS

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tenant"] = self.request.active_tenant
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Avaliacao fisica atualizada com sucesso.")
        return super().form_valid(form)


class PhysicalAssessmentDeleteView(TenantObjectPermissionMixin, DeleteView):
    model = PhysicalAssessment
    template_name = "shared/confirm_delete.html"
    success_url = reverse_lazy("assessments:physical_list")
    required_tenant_permission = TenantPermissions.ASSESSMENTS

    def form_valid(self, form):
        messages.success(self.request, "Avaliacao fisica excluida com sucesso.")
        return super().form_valid(form)


class PosturalAssessmentListView(TenantPermissionRequiredMixin, ListView):
    model = PosturalAssessment
    template_name = "assessments/postural_list.html"
    context_object_name = "assessments"
    paginate_by = 12
    required_tenant_permission = TenantPermissions.ASSESSMENTS


class PosturalAssessmentCreateView(TenantPermissionRequiredMixin, CreateView):
    model = PosturalAssessment
    form_class = PosturalAssessmentForm
    template_name = "assessments/postural_form.html"
    success_url = reverse_lazy("assessments:postural_list")
    required_tenant_permission = TenantPermissions.ASSESSMENTS

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tenant"] = self.request.active_tenant
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Avaliacao postural registrada com sucesso.")
        return super().form_valid(form)


class PosturalAssessmentUpdateView(TenantObjectPermissionMixin, UpdateView):
    model = PosturalAssessment
    form_class = PosturalAssessmentForm
    template_name = "assessments/postural_form.html"
    success_url = reverse_lazy("assessments:postural_list")
    required_tenant_permission = TenantPermissions.ASSESSMENTS

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tenant"] = self.request.active_tenant
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Avaliacao postural atualizada com sucesso.")
        return super().form_valid(form)


class PosturalAssessmentDeleteView(TenantObjectPermissionMixin, DeleteView):
    model = PosturalAssessment
    template_name = "shared/confirm_delete.html"
    success_url = reverse_lazy("assessments:postural_list")
    required_tenant_permission = TenantPermissions.ASSESSMENTS

    def form_valid(self, form):
        messages.success(self.request, "Avaliacao postural excluida com sucesso.")
        return super().form_valid(form)
